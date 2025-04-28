# Santa Monica
#### Video Demo:  <[URL HERE](https://youtu.be/9I3WQC3JRm4)>
#### Description:
My final project is a web-based application developed using Flask, JavaScript, Python, HTML, CSS, Bootstrap, and SQL.

Santa Monica is a family-owned restaurant website that features essential restaurant pages such as Home, Menu, About, Contact, Shopping Cart, Register, Login, and Logout. A key feature of the website is the shopping cart, allowing users to order pizza within Manchester or opt for collection if their postcode is outside the delivery area.

The website is fully responsive and works seamlessly across various devices, including desktop computers, laptops, tablets, and smartphones.

Technical Details

I used Flask to create a layout.html template, enabling dynamic reuse of the layout across multiple pages. This approach simplifies development and enhances maintainability. For example, if a user is logged in, the navigation menu dynamically updates to display a Logout option. Other Flask features, such as routing and session management, have also been implemented to handle user interactions effectively.

Shopping Cart Functionality

The shopping cart is the standout feature of the website. Users can choose from categories such as Pizza, Sides, and Drinks to add items to their cart. The number of items in the cart is displayed dynamically on the navigation menu, thanks to JavaScript. This allows for real-time updates without requiring page reloads, improving user experience and optimizing performance. Unlike Flask’s render_template function, which requires reloading the entire page, JavaScript facilitates efficient client-side updates.

All item details, including pictures, descriptions, and prices, are stored in an SQLite3 database. This ensures data consistency and allows for easy updates to the menu.

Checkout Process

Once items are added to the shopping cart, users can proceed to the checkout page. However, only logged-in users can access the checkout. If a user is not logged in, they are redirected to the registration page. Upon successful registration, they are redirected to the login page. Only after logging in can the user proceed to checkout.

On the checkout page, users must fill out a form with the following details:

- Full Name
- Email Address
- Phone Number
- Delivery Address

If the provided postcode is outside Manchester, the user can only select the collection option, as delivery is limited to Manchester. Users can choose to pay by card or cash, and the total order amount is displayed at the bottom of the checkout form before the confirmation button.

Email Confirmation

After placing an order successfully, the user receives an email confirmation, which is implemented using Flask-Mail. For confidentiality, sensitive information such as the email address and password used for the mail server is not disclosed.

Key Features:

- Responsive Design: The website is fully responsive and adapts to various screen sizes, providing an optimal user experience on all devices.

- Dynamic Navigation: The navigation menu updates based on the user’s authentication status.

- Shopping Cart: Real-time cart updates using JavaScript enhance user experience.

- Database Integration: Menu items are stored in an SQLite3 database, allowing for easy updates and scalability.

- Checkout Validation: Only registered and logged-in users can complete the checkout process.

- Email Notifications: Order confirmations are sent via email, ensuring users receive a record of their transactions.

Challenges and Learnings:

One of the main challenges was implementing the dynamic shopping cart functionality. Initially, I relied heavily on Flask’s render_template for updates, which required reloading the page every time an item was added or removed from the cart. Switching to JavaScript for dynamic updates significantly improved the performance and user experience.

Another challenge was ensuring secure email notifications. Using Flask-Mail required careful handling of credentials and server configurations to maintain security and privacy.

Future Improvements:

- Admin Panel: Develop an admin panel for managing menu items and orders directly through the website.

- Delivery Tracking: Integrate a tracking feature for users to monitor the status of their orders.

- Payment Gateway: Implement a secure payment gateway for online card transactions.

- User Profiles: Allow users to save their details and view order history.

This project demonstrates my ability to develop a full-stack web application, combining frontend and backend technologies to create a user-friendly and functional product. The knowledge gained from this project has strengthened my skills in Flask, database management, JavaScript, and responsive design.


