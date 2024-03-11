
import streamlit as st
import pandas as pd

# Sample room data (initially empty for lister submissions)
room_data = pd.DataFrame(columns=['room_id', 'title', 'description', 'location', 'price', 'image', 'virtual_tour', 'dimensions'])

# Sample furniture data
furniture_data = pd.DataFrame({
    'name': ['Chair', 'Table', 'Bed'],
    'image': ['https://via.placeholder.com/150', 'https://via.placeholder.com/150', 'https://via.placeholder.com/150'],
    'length': [2, 4, 6],
    'width': [2, 3, 4],
    'height': [3, 2, 2]
})

# Function to display room information
def display_room_info(room):
    st.image(room['image'], caption=room['title'], use_column_width=True)
    st.write(f"**Location:** {room['location']}")
    st.write(f"**Description:** {room['description']}")
    st.write(f"**Price:** ${room['price']}/month")
    st.write(f"**Dimensions:** {room['dimensions']}")
    st.write(f"**Virtual Tour:** [Virtual Tour Link]({room['virtual_tour']})")

# Function to display furniture images
def display_furniture_images(furniture_data):
    for idx, row in furniture_data.iterrows():
        st.image(row['image'], caption=row['name'], width=150)

# Main Streamlit app
def main():
    
    st.title('Demo App')
    st.title('only for demo purpose')

    # Sidebar - User Type Selection
    user_type = st.sidebar.radio("Login as", ('Lister', 'Finder', "Design Planner"))

    if user_type == 'Lister':
        st.sidebar.title('Lister Login')
        # Lister login form (placeholder)
        email = st.sidebar.text_input("Email")
        password = st.sidebar.text_input("Password", type="password")
        st.sidebar.button("Login")

        # Lister Dashboard
        st.header('Lister Dashboard')
        st.subheader('List a New Room')

        # Lister Room Listing Form
        with st.form("room_listing_form"):
            title = st.text_input("Title")
            description = st.text_area("Description")
            location = st.text_input("Location")
            price = st.number_input("Price ($/month)", min_value=0)
            virtual_tour = st.text_input("Virtual Tour Link")
            dimensions = st.text_input("Dimensions")

            # Submit button
            submitted = st.form_submit_button("Submit Listing")

            if submitted:
                # Add new room to room_data
                new_room_id = len(room_data) + 1
                new_room = {
                    'room_id': new_room_id,
                    'title': title,
                    'description': description,
                    'location': location,
                    'price': price,
                    'image': 'https://via.placeholder.com/300',
                    'virtual_tour': virtual_tour,
                    'dimensions': dimensions
                }
                room_data.loc[len(room_data)] = new_room
                st.success("Room listing submitted successfully!")

        st.subheader('Your Listings')
        for idx, room in room_data.iterrows():
            st.write(f"## {room['title']}")
            display_room_info(room)
            st.write("---")

    elif user_type == 'Finder':
        st.sidebar.title('Finder Login')
        # Finder login form (placeholder)
        email = st.sidebar.text_input("Email")
        password = st.sidebar.text_input("Password", type="password")
        st.sidebar.button("Login")

        # Main content - Finder Explore Rooms
        st.header('Explore Rooms')
        st.write("Use the filters below to find your ideal room:")
        
        # Filter by Location
        location_filter = st.selectbox("Location", room_data['location'].unique())
        filtered_rooms = room_data[room_data['location'] == location_filter]

        # Display filtered rooms
        for idx, room in filtered_rooms.iterrows():
            st.write(f"## {room['title']}")
            display_room_info(room)
            if st.button(f"View Details for {room['title']}"):
                st.subheader(f"Details for {room['title']}")
                display_room_info(room)
                st.warning("You can now plan the layout!")
                if st.button("Plan Layout"):
                    st.header("Room Layout Planning")
                    st.write("Select furniture to plan the layout:")
                    selected_furniture = st.selectbox("Select Furniture:", furniture_data['name'])
                    display_furniture_images(furniture_data[furniture_data['name'] == selected_furniture])
                    st.write(f"**Dimensions:** Length: {furniture_data.loc[furniture_data['name'] == selected_furniture, 'length'].values[0]} ft, "
                            f"Width: {furniture_data.loc[furniture_data['name'] == selected_furniture, 'width'].values[0]} ft, "
                            f"Height: {furniture_data.loc[furniture_data['name'] == selected_furniture, 'height'].values[0]} ft")

                    # Image uploader for room background
                    uploaded_room_image = st.file_uploader("Upload Image of Room Background", type=["jpg", "jpeg", "png"])
                    
                    if uploaded_room_image is not None:
                        st.image(uploaded_room_image, caption='Room Background', use_column_width=True)

                        # Display selected furniture in the room
                        st.write("Plan your room layout:")
                        furniture_location = st.image(uploaded_room_image, caption='Room with Furniture', use_column_width=True)

                        # Get selected furniture dimensions
                        selected_length = furniture_data.loc[furniture_data['name'] == selected_furniture, 'length'].values[0]
                        selected_width = furniture_data.loc[furniture_data['name'] == selected_furniture, 'width'].values[0]
                        selected_height = furniture_data.loc[furniture_data['name'] == selected_furniture, 'height'].values[0]

                        # Allow users to drag and drop furniture
                        left, top = st.columns(2)
                        with left:
                            st.write("Furniture Dimensions:")
                            st.write(f"Length: {selected_length} ft")
                            st.write(f"Width: {selected_width} ft")
                            st.write(f"Height: {selected_height} ft")

                        with top:
                            st.write("Drag and drop furniture items onto the room background:")
                            x, y = st.image_coordinates(uploaded_room_image, label="Drag furniture here", use_container_width=True, key="furniture")

                            if st.button("Place Furniture"):
                                furniture_location.empty()
                                st.image(uploaded_room_image,  caption='Room with Furniture', use_column_width=True)
                                st.write(f"Placed {selected_furniture} at position: ({x}, {y})")

                        # Virtual Tour Section
                        st.header("Virtual Tour")
                        st.write("Take a virtual tour of the room:")
                        st.video(room['virtual_tour'])

                        # Communal Area Exploration Section (Placeholder)
                        st.header('Communal Area Exploration')
                        st.write("Explore communal areas virtually:")
                        st.write("Coming soon...")

        # Communal Area Exploration Section (Placeholder)
        st.header('Communal Area Exploration')
        st.write("Explore communal areas virtually:")
        st.write("Coming soon...")

    elif user_type == 'Design Planner':
        st.sidebar.title('Design Planner Login')
        # Design Planner login form (placeholder)
        email = st.sidebar.text_input("Email")
        password = st.sidebar.text_input("Password", type="password")
        st.sidebar.button("Login")
        st.sidebar.title("add furniture items")
        # Main content - Design Planning
        st.header('Design Planning')
        st.write("Welcome to the Design Planner!")

        # Placeholder for storing placed furniture
        placed_furniture = []
        
        # Select furniture for optimal placement
        st.subheader("Select Furniture for Placement:")
        selected_furniture = st.selectbox("Select Furniture:", furniture_data['name'])

        # Machine Learning Placeholder (Optimal Placement)
        if st.button("Find Optimal Placement"):
            st.write("Finding optimal placement...")
            # Placeholder for machine learning algorithm to find optimal placement
            optimal_x = 5  # Example: x-coordinate
            optimal_y = 5  # Example: y-coordinate
            st.success(f"Optimal placement for {selected_furniture}: ({optimal_x}, {optimal_y})")

            # Add placed furniture to the list
            placed_furniture.append({
                'name': selected_furniture,
                'x_position': optimal_x,
                'y_position': optimal_y
            })

            # Display placed furniture
            st.subheader("Placed Furniture:")
            for furniture in placed_furniture:
                st.write(f"- {furniture['name']} at position: ({furniture['x_position']}, {furniture['y_position']})")

        # Display room layout with placed furniture
        st.subheader("Room Layout with Placed Furniture:")
        room_image = st.image('https://via.placeholder.com/600x400', caption='Room with Placed Furniture', use_column_width=True)

        # User interaction to place additional furniture
        st.subheader("Add More Furniture:")
        #new_furniture_name = st.selectbox("Select Furniture:", furniture_data['name'])
        new_furniture_x = st.slider("X Position:", min_value=0, max_value=10, step=1, value=5)
        new_furniture_y = st.slider("Y Position:", min_value=0, max_value=10, step=1, value=5)

        # Add new furniture when button is clicked
        if st.button("Add Furniture"):
            pass
            # placed_furniture.append({
            #     'name': new_furniture_name,
            #     'x_position': new_furniture_x,
            #     'y_position': new_furniture_y
            # })
            # st.success(f"{new_furniture_name} added at position: ({new_furniture_x}, {new_furniture_y})")

        # Update room image with all placed furniture
        # updated_room_image_url = 'https://via.placeholder.com/600x400'  # Placeholder for updated room image
        # room_image.image(updated_room_image_url, caption='Room with Placed Furniture', use_column_width=True)

        # Display all placed furniture
        st.subheader("All Placed Furniture:")
        for furniture in placed_furniture:
            st.write(f"- {furniture['name']} at position: ({furniture['x_position']}, {furniture['y_position']})")

    # About Section
    st.sidebar.markdown("---")
    st.sidebar.write("About")
    st.sidebar.info(
        "This app allows users to find and customize their ideal room virtually. "
        "Listers can upload room listings with virtual tours and dimensions. "
        "Finders can explore rooms, customize with furniture, take virtual tours, and explore communal areas. "
        "Design Planners can use intuitive tools to plan optimal furniture placement in rooms."
    )

if __name__ == '__main__':
    main()
