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
        ticker_dir = self.cache_dir / ticker.replace('/', '_')
        ticker_dir.mkdir(exist_ok=True)
        return ticker_dir / f"{field.lower().replace(' ', '_')}.csv"
    
    def _load_cached_data(self, ticker, field):
        """Load existing data from cache if available"""
        cache_path = self._get_cache_path(ticker, field)
        if cache_path.exists():
            # Explicitly specify index_col=0 and parse_dates=True
            df = pd.read_csv(
                cache_path,
                index_col=0,
                parse_dates=True
            )
            return df
        return None
    
    def _save_to_cache(self, ticker, field, data):
        """Save data to cache file"""
        # Ensure data has a datetime index
        if not isinstance(data.index, pd.DatetimeIndex):
            data.index = pd.to_datetime(data.index)
        
        # Ensure data is a DataFrame
        if isinstance(data, pd.Series):
            data = data.to_frame(name=field)
        
        cache_path = self._get_cache_path(ticker, field)
        # Save with datetime index
        data.to_csv(cache_path, date_format='%Y-%m-%d')
    
    def _prepare_bloomberg_data(self, data, field):
        """Prepare Bloomberg data for storage by ensuring proper format"""
        if isinstance(data, pd.Series):
            data = data.to_frame(name=field)
        elif isinstance(data, pd.DataFrame):
            if data.columns.size == 1:
                data.columns = [field]
        
        # Ensure datetime index
        if not isinstance(data.index, pd.DatetimeIndex):
            data.index = pd.to_datetime(data.index)
        
        return data
    
    def get_timeseries(self, bloomberg_client, ticker, fields, start_date, end_date):
        """
        Get timeseries data for a ticker and multiple fields, using cache when available
        and fetching missing data from Bloomberg when necessary
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
                    result_data[field] = cached_data
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
                        field_data = self._prepare_bloomberg_data(new_data[field], field)
                        self._save_to_cache(ticker, field, field_data)
                        result_data[field] = field_data
        
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
                    field_data = self._prepare_bloomberg_data(range_data[field], field)
                    new_data_frames.append(field_data)
            
            if new_data_frames:
                # Combine cached data with new data
                all_data = pd.concat([cached_data] + new_data_frames)
                all_data = all_data.sort_index().drop_duplicates()
                self._save_to_cache(ticker, field, all_data)
                result_data[field] = all_data
            else:
                result_data[field] = cached_data
        
        # Combine all fields into a single DataFrame
        if not result_data:
            return pd.DataFrame()
        
        # Combine all fields and ensure proper datetime index
        final_df = pd.concat(result_data.values(), axis=1)
        final_df.columns = result_data.keys()
        final_df.index = pd.to_datetime(final_df.index)
        final_df = final_df.sort_index()
        
        return final_df.loc[start_date:end_date]
