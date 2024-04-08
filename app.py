import plotly.express as px
import seaborn as sns
from shiny.express import input, ui
from shiny import render
from shinywidgets import render_plotly, render_widget
import palmerpenguins
from shiny import reactive, render, req
import shinyswatch
from palmerpenguins import load_penguins
import seaborn as sns
from shiny import reactive, render
from faicons import icon_svg
import json
import pathlib
from ipyleaflet import Map, Marker
# Theme
shinyswatch.theme.darkly()

# Built-in function to load the penguin dataset
penguins_df = palmerpenguins.load_penguins()

# Title for chart
ui.page_opts(title="WILD PENGUIN DATA", fillable=True,)

# Add a Shiny UI sidebar for user interaction
with ui.sidebar(open='open'):
        
        ui.h1("Penguin Data Options 🏝️")
        with ui.accordion():
            with ui.accordion_panel("🐧 Penguin Specs Selection"):
                ui.input_selectize("selected_attribute", "Select an attribute:", 
                          ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"])
            with ui.accordion_panel("📊 Histogram"):
                ui.input_numeric("plotly_bin_count", "Plotly Histogram Bins:", value=20, min=1, max=100)
            with ui.accordion_panel("📈 Seaborn Bins Slider"):
                ui.input_slider("seaborn_bin_count", "# of Seaborn Bins:", min=1, max=50, value=10)
            with ui.accordion_panel("🧬 Species Filter"):
                ui.input_checkbox_group("selected_species_list", "Filter by Species:", 
                                choices=["Adelie", "Gentoo", "Chinstrap"], 
                                selected=["Adelie", "Gentoo", "Chinstrap"], inline=True)
            with ui.accordion_panel("🏔️ Island Filter"):
                ui.input_checkbox_group("selected_island_list", "Filter by Island:", 
                                choices=["Torgersen", "Biscoe", "Dream"], 
                                selected=["Torgersen", "Biscoe", "Dream"], inline=True)
            with ui.accordion_panel("📏 Bill Length Filter"):
                ui.input_slider("bill_length_mm", "Length (mm)", 30, 60, 60)


# Data Content

# Data Table and Data Grid
with ui.card():
        with ui.layout_columns():
            with ui.value_box(showcase= icon_svg('feather'), max_height="300px", theme="bg-gradient-blue-green"):
                "Total Penguins Filtered"
                @render.text
                def display_penguin_count():
                    df = filtered_data()
                    return f"{len(df)} penguins"

            with ui.value_box(showcase=icon_svg("ruler-horizontal"), max_height="300px", theme="bg-gradient-blue-green"):
                "Average Bill Length"
                @render.text
                def average_bill_length():
                    df = filtered_data()
                    return f"{df['bill_length_mm'].mean():.2f} mm" if not df.empty else "N/A"

            with ui.value_box(showcase=icon_svg("ruler-vertical"), max_height="300px", theme="bg-gradient-blue-green"):
                "Average Bill Depth"
                @render.text
                def average_bill_depth():
                    df = filtered_data()
                    return f"{df['bill_depth_mm'].mean():.2f} mm" if not df.empty else "N/A"

with ui.layout_columns():
    with ui.accordion(id="acc",open="closed"):
        with ui.accordion_panel("Data Table"):
            @render.data_frame
            def penguin_datatable():
                return render.DataTable(filtered_data())

        with ui.accordion_panel("Data Grid"):
            @render.data_frame
            def penguin_datagrid():
                return render.DataGrid(filtered_data())

# Display Plotly histogram
with ui.navset_card_tab(id="tab"):
    with ui.nav_panel("Plotly Histogram"):

        @render_plotly
        def plotly_histogram():
            plotly_hist = px.histogram(
                data_frame=filtered_data(),
                x=input.selected_attribute(),
                nbins=input.plotly_bin_count(),
                color="species",
            ).update_layout(
                title="Plotly Penguins Data",
                xaxis_title="Selected Attribute",
                yaxis_title="Count",
            )
            
            return plotly_hist

# Display Seaborn histogram    
    with ui.nav_panel("Seaborn Histogram"):
        @render.plot
        def seaborn_histogram():
            histplot = sns.histplot(data=filtered_data(), x="body_mass_g", bins=input.seaborn_bin_count())
            histplot.set_title("Palmer Penguins")
            histplot.set_xlabel("Mass")
            histplot.set_ylabel("Count")
            sns.set_style('darkgrid')
            return histplot

# Display Plotly Scatterplot
    with ui.nav_panel("Plotly Scatterplot"):
        ui.card_header("Plotly Scatterplot: Species")

        @render_plotly
        def plotly_scatterplot():
            return px.scatter(
                filtered_data(),
                x="body_mass_g",
                y="bill_length_mm",
                color="species",
                 color_discrete_map={
                     'Adelie': 'blue',
                     'Chinstrap': 'green',
                     'Gentoo': 'red'},
            )
# Display Map
    with ui.nav_panel("Map"):
        ui.card_header("Island Map")

        @render_widget
        def Island_map(width="100%", height="100px"):
            return Map(center=(-67.7675, -59.8467), zoom=4,)

@reactive.calc
@reactive.calc
def filtered_data():
    return penguins_df[penguins_df["species"].isin(input.selected_species_list())]
