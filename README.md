# E-Commerce Website Project
## Overview
This e-commerce project is a feature-rich web application built using Python and Django, offering a seamless shopping experience for customers. It includes a range of functionalities that empower users to shop, manage their orders, interact with blogs, and handle user authentication. Furthermore, this project is designed with an eye on the future, as it provides API endpoints to support a forthcoming mobile application.

## Key Features
- Product Catalog: Customers can browse a wide range of products and select items they wish to purchase.
- Shopping Cart: Users can add products to their cart, review their selections, and proceed to checkout.
- Order History: Customers can view their order history to keep track of past purchases.
- User Profile Management: Users can update their profiles and manage personal information.
- Order Tracking: The system allows users to track the status of their orders, providing real-time updates.
- Blog Section: The project incorporates a blog section for informative and engaging content.
- User Authentication: Secure user authentication ensures user data is protected.
- API Support: API endpoints are provided to facilitate future integration with a mobile application.

## Technologies Used
- Programming Languages: Python
- Web Framework: Django
- API Framework: Django Rest Framework
- Database: SQL Lite
- Payment Gateway: Razor Pay

## Project Description
- This e-commerce website is a sophisticated and user-friendly platform that simplifies online shopping. Customers can effortlessly browse, select, and purchase products, all while enjoying a smooth and secure experience. With features like order tracking, order history, user profiles, and informative blogs, the site offers a comprehensive shopping experience.
- Built on the Python and Django stack, this project leverages the robust Django Rest Framework to expose API endpoints for potential integration with a mobile app. The use of SQL Lite ensures data is efficiently managed, and Razor Pay integration guarantees secure and convenient payment processing.
- This project demonstrates our commitment to creating a feature-rich and scalable e-commerce solution that meets the needs of both customers and the business. It offers a strong foundation for future expansion and enhancements, making it a valuable asset to the e-commerce landscape.
- 

## Project Setup
1. Clone github repository
```sh
git clone <project> 
```
2. Create virtual envirnoment
Windows:
```sh
    python -m venv <env name>
```
Linux/Unix:
```sh
    pip install virtualenv
    virtualenv <env name>
```
3. Activate virtual envirnoment
Windows:
```sh
<env name>/scripts/activate
```
Linux/Unix:
```sh
<env name>/bin/activate
```
4. Run migrations:
```sh
python manage.py makemigrations
python manage.py migrate
```
5. Run development server on port
```sh
python manage.py runserver
```
on custom port run,
```sh
python manage.py runserver <Port Number>
```
