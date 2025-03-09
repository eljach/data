def get_timeseries(self, bloomberg_client, ticker, fields, start_date, end_date):
    """
    Get timeseries data for a ticker and fields, using cache when available
    and fetching missing data from Bloomberg when necessary
    """
    # Convert dates to datetime if they're strings
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    result_data = {}
    
    # Handle single field case
    if isinstance(fields, str):
        fields = [fields]
    
    for field in fields:
        # Load cached data if available
        cached_data = self._load_cached_data(ticker, field)
        
        if cached_data is not None:
            # Check if we need to fetch any missing data
            missing_ranges = []
            
            # Check if we need data before the cached range
            if start_date < cached_data.index.min():
                missing_ranges.append((start_date, cached_data.index.min() - pd.Timedelta(days=1)))
            
            # Check if we need data after the cached range
            if end_date > cached_data.index.max():
                missing_ranges.append((cached_data.index.max() + pd.Timedelta(days=1), end_date))
            
            if missing_ranges:
                new_data_pieces = [cached_data]  # Start with existing cached data
                
                for missing_start, missing_end in missing_ranges:
                    # Fetch missing data from Bloomberg
                    new_data = bloomberg_client.get_timeseries(
                        ticker, 
                        [field],
                        missing_start, 
                        missing_end
                    )
                    
                    if new_data is not None and field in new_data:
                        field_data = new_data[field]
                        if isinstance(field_data, pd.Series):
                            field_data = field_data.to_frame(name=field)
                        new_data_pieces.append(field_data)
                
                # Combine all pieces of data
                if len(new_data_pieces) > 1:
                    # Concatenate all pieces and sort by date
                    all_data = pd.concat(new_data_pieces)
                    all_data = all_data.sort_index()
                    # Remove any potential duplicates
                    all_data = all_data[~all_data.index.duplicated(keep='first')]
                    
                    # Save the complete dataset back to cache
                    self._save_to_cache(ticker, field, all_data)
                    
                    result_data[field] = all_data
                else:
                    result_data[field] = cached_data
            else:
                result_data[field] = cached_data
        else:
            # No cached data exists, fetch everything from Bloomberg
            new_data = bloomberg_client.get_timeseries(
                ticker, 
                [field],
                start_date, 
                end_date
            )
            
            if new_data is not None and field in new_data:
                field_data = new_data[field]
                if isinstance(field_data, pd.Series):
                    field_data = field_data.to_frame(name=field)
                self._save_to_cache(ticker, field, field_data)
                result_data[field] = field_data
    
    # Combine all fields into a single DataFrame
    if len(result_data) > 0:
        final_df = pd.concat(result_data.values(), axis=1)
        final_df.columns = result_data.keys()
        # Return only the requested date range
        return final_df.loc[start_date:end_date]
    else:
        return pd.DataFrame()
