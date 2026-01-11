# Santa Monica – Full-Stack Restaurant Ordering System

A full-stack web application for a family-owned restaurant, designed to support online food ordering with authentication, shopping cart functionality, and order confirmation.

Built as a production-style project to reflect real restaurant business requirements, including delivery rules, user accounts, and order processing.

---

## 🔹 Project Overview

Santa Monica is a responsive restaurant website that allows customers to browse the menu, create an account, add items to a shopping cart, and place orders for delivery or collection.

Delivery availability is restricted by postcode, simulating real-world operational constraints. Only authenticated users can complete checkout, ensuring controlled access and data integrity.

---

## 🔹 Key Features

- User registration, login, and session-based authentication  
- Dynamic shopping cart with real-time updates  
- Menu items stored and managed via database  
- Delivery or collection logic based on postcode  
- Secure checkout flow for authenticated users only  
- Email order confirmation using server-side email service  
- Fully responsive design across all devices  

---

## 🔹 Tech Stack

**Frontend**
- HTML5
- CSS3
- Bootstrap
- JavaScript (Vanilla)

**Backend**
- Python
- Flask
- SQLite
- Flask-Mail

---

## 🔹 My Role

- Designed and developed the application end-to-end  
- Implemented authentication, session handling, and access control  
- Built dynamic cart functionality using JavaScript for improved UX  
- Integrated database-driven menu and order logic  
- Implemented email notifications for order confirmation  

---

## 🔹 Architecture Highlights

- Flask templating with a reusable base layout  
- Session-based authentication with dynamic navigation  
- Client-side cart updates to reduce unnecessary page reloads  
- Server-side validation for checkout and delivery logic  

---

## 🔹 Challenges & Learnings

One of the main challenges was implementing a responsive and efficient shopping cart. Early versions relied on server-side rendering, which caused full page reloads. Migrating cart updates to JavaScript significantly improved performance and user experience.

Another key learning was handling secure email notifications and protecting sensitive configuration data within the backend.

---

## 🔹 Future Improvements

- Admin dashboard for order and menu management  
- Online payment gateway integration  
- Order history and user profiles  
- Order status tracking  

---

## 🔹 Notes

This project was developed as part of the **CS50 final project**, with a focus on building a real-world, full-stack web application rather than a purely academic exercise.

It demonstrates practical experience with backend development, authentication, database design, and user-focused frontend functionality.
