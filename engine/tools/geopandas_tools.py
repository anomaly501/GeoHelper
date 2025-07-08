# engine/tools/geopandas_tools.py
import geopandas as gpd
import os

def read_file(filename: str, **kwargs):
    """Wrapper for geopandas.read_file."""
    print(f"TOOL: Reading file '{filename}'")
    return gpd.read_file(filename, **kwargs)

def buffer(gdf: gpd.GeoDataFrame, output_path: str, distance: float, **kwargs):
    """
    Wrapper for GeoDataFrame.buffer.
    Assumes data is in a projected CRS for distance in meters.
    """
    print(f"TOOL: Buffering data by {distance} units.")
    # In a real system, you might add a CRS check here.
    buffered_gdf = gdf.copy()
    buffered_gdf['geometry'] = gdf.geometry.buffer(distance, **kwargs)
    
    print(f"TOOL: Saving buffer result to '{output_path}'")
    buffered_gdf.to_file(output_path, driver='GeoJSON')
    return output_path # Return the path to the created file

def to_file(gdf: gpd.GeoDataFrame, output_path: str, **kwargs):
    """Wrapper for GeoDataFrame.to_file."""
    print(f"TOOL: Saving GeoDataFrame to '{output_path}'")
    gdf.to_file(output_path, **kwargs)
    return output_path