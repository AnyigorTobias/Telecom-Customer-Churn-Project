import numpy as np
import plotly.graph_objects as go
import streamlit as st

# Define the sigmoid function
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Generate x values
x_values = np.linspace(-10, 10, 400)

# Calculate y values using the sigmoid function
y_values = sigmoid(x_values)

# Create Plotly figure
fig = go.Figure()

# Add sigmoid trace
fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='lines', name='Sigmoid'))

# Set layout
fig.update_layout(title='Sigmoid Function',
                  xaxis_title='x',
                  yaxis_title='y',
                  template='plotly_white')

# Streamlit app
st.title('Interactive Sigmoid Function')
st.plotly_chart(fig, use_container_width=True)
