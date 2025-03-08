import pandas as pd
import os
from datetime import datetime
from pathlib import Path

class BloombergDataCache:
    def __init__(self, cache_dir="data_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
    
    def _get_cache_path(self, ticker):
        """Generate a standardized cache file path for a given ticker"""
        return self.cache_dir / f"{ticker.replace('/', '_')}_data.csv"
    
    def _load_cached_data(self, ticker):
        """Load existing data from cache if available"""
        cache_path = self._get_cache_path(ticker)
        if cache_path.exists():
            df = pd.read_csv(cache_path, parse_dates=['date'])
            df.set_index('date', inplace=True)
            return df
        return None
    
    def _save_to_cache(self, ticker, data):
        """Save data to cache file"""
        cache_path = self._get_cache_path(ticker)
        data.to_csv(cache_path)
    
    def get_timeseries(self, bloomberg_client, ticker, start_date, end_date):
        """
        Get timeseries data for a ticker, using cache when available and
        fetching missing data from Bloomberg when necessary
        """
        # Convert dates to datetime if they're strings
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        
        # Load cached data if available
        cached_data = self._load_cached_data(ticker)
        
        if cached_data is not None:
            # Check if we need to fetch any missing data
            missing_ranges = []
            
            # Check if we need data before the cached range
            if start_date < cached_data.index.min():
                missing_ranges.append((start_date, cached_data.index.min()))
            
            # Check if we need data after the cached range
            if end_date > cached_data.index.max():
                missing_ranges.append((cached_data.index.max(), end_date))
            
            # If we have missing ranges, fetch them from Bloomberg
            if missing_ranges:
                new_data_frames = []
                for missing_start, missing_end in missing_ranges:
                    # Fetch missing data from Bloomberg
                    new_data = bloomberg_client.get_timeseries(
                        ticker, 
                        missing_start, 
                        missing_end
                    )
                    if new_data is not None:
                        new_data_frames.append(new_data)
                
                # Combine cached data with new data
                if new_data_frames:
                    all_data = pd.concat([cached_data] + new_data_frames)
                    all_data = all_data.sort_index().drop_duplicates()
                    # Save updated data to cache
                    self._save_to_cache(ticker, all_data)
                else:
                    all_data = cached_data
            else:
                all_data = cached_data
        else:
            # No cached data exists, fetch everything from Bloomberg
            all_data = bloomberg_client.get_timeseries(ticker, start_date, end_date)
            if all_data is not None:
                self._save_to_cache(ticker, all_data)
        
        # Return only the requested date range
        return all_data.loc[start_date:end_date]


cache = BloombergDataCache(cache_dir="bloomberg_cache")
bloomberg_client = YourBloombergClient()  # Your existing client

# Get data (will use cache when available)
data = cache.get_timeseries(
    bloomberg_client,
    ticker="AAPL US Equity",
    start_date="2020-01-01",
    end_date="2023-12-31"
)
