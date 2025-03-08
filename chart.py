import pandas as pd
import os
from datetime import datetime
from pathlib import Path

class BloombergDataCache:
    def __init__(self, cache_dir="data_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
    
    def _get_cache_path(self, ticker, field):
        """Generate a standardized cache file path for a given ticker and field"""
        # Create a subdirectory for the ticker to group all its fields
        ticker_dir = self.cache_dir / ticker.replace('/', '_')
        ticker_dir.mkdir(exist_ok=True)
        # Store each field in a separate file
        return ticker_dir / f"{field.lower().replace(' ', '_')}.csv"
    
    def _load_cached_data(self, ticker, field):
        """Load existing data from cache if available"""
        cache_path = self._get_cache_path(ticker, field)
        if cache_path.exists():
            df = pd.read_csv(cache_path, parse_dates=['date'])
            df.set_index('date', inplace=True)
            return df
        return None
    
    def _save_to_cache(self, ticker, field, data):
        """Save data to cache file"""
        cache_path = self._get_cache_path(ticker, field)
        data.to_csv(cache_path)
    
    def get_timeseries(self, bloomberg_client, ticker, fields, start_date, end_date):
        """
        Get timeseries data for a ticker and multiple fields, using cache when available
        and fetching missing data from Bloomberg when necessary
        
        Parameters:
        -----------
        bloomberg_client : Your Bloomberg API client
        ticker : str
            The Bloomberg ticker
        fields : str or list
            Single field or list of fields to retrieve
        start_date : str or datetime
            Start date for the data
        end_date : str or datetime
            End date for the data
        
        Returns:
        --------
        dict : Dictionary of DataFrames, keyed by field
        """
        # Convert fields to list if it's a single string
        if isinstance(fields, str):
            fields = [fields]
        
        # Convert dates to datetime if they're strings
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        
        result_data = {}
        fields_to_fetch = []
        missing_ranges_by_field = {}
        
        # First, check cache for each field and identify missing data
        for field in fields:
            cached_data = self._load_cached_data(ticker, field)
            
            if cached_data is not None:
                missing_ranges = []
                
                # Check if we need data before the cached range
                if start_date < cached_data.index.min():
                    missing_ranges.append((start_date, cached_data.index.min()))
                
                # Check if we need data after the cached range
                if end_date > cached_data.index.max():
                    missing_ranges.append((cached_data.index.max(), end_date))
                
                if missing_ranges:
                    missing_ranges_by_field[field] = {
                        'cached_data': cached_data,
                        'ranges': missing_ranges
                    }
                else:
                    # If no missing ranges, we can use cached data directly
                    result_data[field] = cached_data.loc[start_date:end_date]
            else:
                # No cached data exists, need to fetch everything
                fields_to_fetch.append(field)
        
        # Fetch any completely missing fields
        if fields_to_fetch:
            new_data = bloomberg_client.get_timeseries(
                ticker, 
                fields_to_fetch,
                start_date,
                end_date
            )
            if new_data is not None:
                for field in fields_to_fetch:
                    if field in new_data:
                        self._save_to_cache(ticker, field, new_data[field])
                        result_data[field] = new_data[field]
        
        # Fetch missing ranges for partially cached fields
        for field, missing_info in missing_ranges_by_field.items():
            cached_data = missing_info['cached_data']
            new_data_frames = []
            
            for missing_start, missing_end in missing_info['ranges']:
                # Fetch missing data from Bloomberg
                range_data = bloomberg_client.get_timeseries(
                    ticker,
                    [field],
                    missing_start,
                    missing_end
                )
                if range_data is not None and field in range_data:
                    new_data_frames.append(range_data[field])
            
            if new_data_frames:
                # Combine cached data with new data
                all_data = pd.concat([cached_data] + new_data_frames)
                all_data = all_data.sort_index().drop_duplicates()
                # Save updated data to cache
                self._save_to_cache(ticker, field, all_data)
                result_data[field] = all_data.loc[start_date:end_date]
            else:
                result_data[field] = cached_data.loc[start_date:end_date]
        
        return result_data
