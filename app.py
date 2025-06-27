import streamlit as st
from db_helper import DB
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


db = DB()
st.set_page_config(layout="wide")

st.sidebar.title('Flights Analytics')
user_option = st.sidebar.selectbox('Menu', ['Select One', 'Check Flights', 'Analytics'])

if user_option == 'Check Flights':
    st.title('Check Flights')

    col1, col2, col3, col4 = st.columns(4)

    cities = db.fetch_city_names()
    scities = db.fetch_Source_city_names()

    with col1:
        source = st.selectbox('Source', ['All'] + sorted(scities))

    with col2:
        if source != 'All':
            valid_destinations = db.fetch_destinations_for_source(source)
        else:
            valid_destinations = cities
        destination = st.selectbox('Destination', ['All'] + sorted(valid_destinations))

    with col3:
        if source != 'All' or destination != 'All':
            months = db.fetch_months_by_route(
                source if source != 'All' else None,
                destination if destination != 'All' else None
            )
        else:
            months = db.fetch_month_names()
        selected_month = st.selectbox('Month', ['All'] + months)

    with col4:
        if source != 'All' or destination != 'All':
            airlines = db.fetch_airlines_by_route(
                source if source != 'All' else None,
                destination if destination != 'All' else None
            )
        else:
            airlines = db.fetch_airline_names()
        airline = st.selectbox('Airlines', ['All'] + sorted(airlines))

    if st.button('Search'):
        results = db.fetch_all_flights(selected_month, airline, source, destination)

        if results:
            st.success(f"Showing {len(results)} matching flights")
            df = pd.DataFrame(results, columns=['Airline', 'Route', 'Dep_Time', 'Duration', 'Price'])
            st.dataframe(df)
        else:
            st.warning("No flights found for the selected criteria.")

elif user_option == 'Analytics':
    st.title("📊 Flights Analytics Dashboard")

    colA, colB = st.columns(2)

    with colA:
        st.subheader("✈️ Flight Share by Airlines")
        airline, frequency = db.fetch_airline_frequency()
        fig_pie = go.Figure(
            go.Pie(
                labels=airline,
                values=frequency,
                hoverinfo="label+percent+value",
                textinfo="percent",
                hole=0.3,
                marker=dict(colors=px.colors.qualitative.Pastel)
            )
        )
        fig_pie.update_layout(title="Airline Market Share")
        st.plotly_chart(fig_pie, use_container_width=True)

    with colB:
        st.subheader("🏙️ Top Airports by Flight Count")
        city, freq = db.busy_airport()
        fig_bar = px.bar(x=city, y=freq, labels={'x': 'City', 'y': 'Flights'}, color=freq, color_continuous_scale='Blues')
        st.plotly_chart(fig_bar, use_container_width=True)

    st.subheader("📈 Daily Flight Volume")
    dates, freq_day = db.daily_frequency()
    fig_line = px.line(x=dates, y=freq_day, markers=True)
    fig_line.update_layout(xaxis_title="Date", yaxis_title="Flights")
    st.plotly_chart(fig_line, use_container_width=True)

    colC, colD = st.columns(2)

    with colC:
        st.subheader("🛣️ Top 10 Busiest Routes")
        routes, route_freq = db.fetch_top_routes()
        fig_routes = px.bar(x=routes, y=route_freq, labels={'x': 'Route', 'y': 'Flights'}, color=route_freq)
        st.plotly_chart(fig_routes, use_container_width=True)

    with colD:
        st.subheader("💰 Avg Ticket Price per Airline")
        air, avg_price = db.fetch_average_price_by_airline()
        fig_price = px.bar(x=air, y=avg_price, labels={'x': 'Airline', 'y': 'Avg Price'}, color=avg_price)
        st.plotly_chart(fig_price, use_container_width=True)

    st.subheader("📆 Monthly Flight Volume")
    months, volume = db.fetch_monthly_volume()
    fig_month = px.line(x=months, y=volume, markers=True)
    fig_month.update_layout(xaxis_title="Month", yaxis_title="Flights")
    st.plotly_chart(fig_month, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Flight Duration Distribution (Histogram)")
        durations = db.fetch_all_durations()
        if durations:
            fig_dur = px.histogram(x=durations, nbins=20, labels={'x': 'Duration (min)', 'y': 'Count'})
            st.plotly_chart(fig_dur, use_container_width=True)
        else:
            st.warning("No duration data available.")

    with col2:
        st.subheader("Total Flight Duration by Airline (Bar Chart)")
        airlines, total_durations = db.fetch_total_duration_by_airline()
        if airlines:
            fig_dur_bar = px.bar(x=airlines, y=total_durations, labels={'x': 'Airline', 'y': 'Total Duration (min)'})
            st.plotly_chart(fig_dur_bar, use_container_width=True)
        else:
            st.warning("No airline duration data available.")

    col3, col4, col5 = st.columns(3)

    with col3:
        #Assume you already have these:
        airlines1, durations1 = db.fetch_airline_duration_between("Banglore" ,"New Delhi")
        airlines2, durations2 = db.fetch_airline_duration_between("Banglore" ,"Delhi")

        fig_pie = make_subplots(
            rows=1, cols=2,
            specs=[[{'type': 'domain'}, {'type': 'domain'}]],
            subplot_titles=["Bangalore To New Delhi", "Bangalore To Delhi"]
        )

        fig_pie.add_trace(
            go.Pie(
                labels=airlines1,
                values=durations1,
                name="New Delhi",
                hoverinfo="label+percent+value",
                textinfo="percent",
                hole=0.3,
                marker=dict(colors=px.colors.qualitative.Pastel)
            ),
            row=1, col=1
        )

        fig_pie.add_trace(
            go.Pie(
                labels=airlines2,
                values=durations2,
                name="Delhi",
                hoverinfo="label+percent+value",
                textinfo="percent",
                hole=0.3,
                marker=dict(colors=px.colors.qualitative.Pastel2)
            ),
            row=1, col=2
        )

        fig_pie.update_layout(
            title_text="Airline Durations by Destination from Bangalore",
            showlegend=False
        )

        st.plotly_chart(fig_pie, use_container_width=True)

    with col4:
        # Assume you already have these:
        airlines1, durations1 = db.fetch_airline_duration_between("Chennai", "Kolkata")
        airlines2, durations2 = db.fetch_airline_duration_between("Delhi", "Cochin")

        fig_pie = make_subplots(
            rows=1, cols=2,
            specs=[[{'type': 'domain'}, {'type': 'domain'}]],
            subplot_titles=["Chennai To Kolkata", "Delhi To Cochin"]
        )

        fig_pie.add_trace(
            go.Pie(
                labels=airlines1,
                values=durations1,
                name="Kolkata",
                hoverinfo="label+percent+value",
                textinfo="percent",
                hole=0.3,
                marker=dict(colors=px.colors.qualitative.Pastel)
            ),
            row=1, col=1
        )

        fig_pie.add_trace(
            go.Pie(
                labels=airlines2,
                values=durations2,
                name="Cochin",
                hoverinfo="label+percent+value",
                textinfo="percent",
                hole=0.3,
                marker=dict(colors=px.colors.qualitative.Pastel2)
            ),
            row=1, col=2
        )

        fig_pie.update_layout(
            title_text="Airline Durations by Destination from Bangalore",
            showlegend=False
        )

        st.plotly_chart(fig_pie, use_container_width=True)

    with col5:
        st.subheader("Total Flight Duration by Airline (Bar Chart)")
        airlines, total_durations = db.fetch_cities_fly_duration()
        if airlines:
            fig_pie = go.Figure(
                go.Pie(
                    labels=airline,
                    values=total_durations,
                    hoverinfo="label+percent+value",
                    textinfo="percent",
                    hole=0.3,
                    marker=dict(colors=px.colors.qualitative.Pastel)
                )
            )
            fig_pie.update_layout(title="Airline Duration from Bangalore to New Delhi")
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.warning("No airline duration data available.")


else:
    st.info("Please select an option from the sidebar to begin.")
