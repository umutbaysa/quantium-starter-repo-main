import pytest
from dash_app import app


def test_header_present(dash_duo):
    # Start the app
    dash_duo.start_server(app)
    
    # Wait for the page to load and find the header
    dash_duo.wait_for_element("h1", timeout=4)
    
    # Find the header element and verify its text
    header = dash_duo.find_element("h1")
    assert header.text == "Pink Morsel Sales Visualizer", \
        "Header should display 'Pink Morsel Sales Visualizer'"
    
    # Verify no console errors
    assert dash_duo.get_logs() == [], "Browser console should contain no errors"


def test_visualization_present(dash_duo):
    # Start the app
    dash_duo.start_server(app)
    
    # Wait for the graph component to be rendered
    dash_duo.wait_for_element("#sales-line-chart", timeout=4)
    
    # Verify the graph element exists
    graph = dash_duo.find_element("#sales-line-chart")
    assert graph is not None, "Sales line chart should be present in the app"
    
    # Verify the graph has been rendered (check for the Plotly structure)
    plotly_graph = dash_duo.find_element("#sales-line-chart .js-plotly-plot")
    assert plotly_graph is not None, "Plotly graph should be fully rendered"
    
    # Verify no console errors
    assert dash_duo.get_logs() == [], "Browser console should contain no errors"


def test_region_picker_present(dash_duo):

    # Start the app
    dash_duo.start_server(app)
    
    # Wait for the region selector to be rendered
    dash_duo.wait_for_element("#region-selector", timeout=4)
    
    # Verify the region selector exists
    region_selector = dash_duo.find_element("#region-selector")
    assert region_selector is not None, "Region selector should be present in the app"
    
    # Verify all expected region options are present
    expected_regions = ['North', 'East', 'South', 'West', 'All']
    
    for region in expected_regions:
        # Find the label elements containing region names
        region_labels = dash_duo.find_elements("label")
        region_texts = [label.text for label in region_labels]
        assert region in region_texts, \
            f"Region option '{region}' should be available in the selector"
    
    # Verify that radio input elements are present
    radio_inputs = dash_duo.find_elements("#region-selector input[type='radio']")
    assert len(radio_inputs) == 5, \
        "Region selector should have 5 radio button options"
    
    # Verify no console errors
    assert dash_duo.get_logs() == [], "Browser console should contain no errors"

