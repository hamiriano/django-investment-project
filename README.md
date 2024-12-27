# Django Investment Project

This project models an investment portfolio system using Django. It includes functionalities for managing assets, portfolios, prices, quantities, and weights.

## Project Structure

- **investment_project/**: Contains the main Django project files.
  - **settings.py**: Configuration settings for the Django project.
  - **urls.py**: URL routing for the project.
  - **wsgi.py**: Entry point for WSGI-compatible web servers.
  - **asgi.py**: Entry point for ASGI-compatible web servers.

- **investment_app/**: Contains the application files.
  - **models.py**: Data models for Activos, Portafolios, Precios, Cantidades, and Weights.
  - **views.py**: View functions or class-based views for handling requests.
  - **urls.py**: URL routing specific to the investment_app.
  - **serializers.py**: Serializers for converting complex data types to JSON.
  - **tests.py**: Test cases for the application.

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd django-investment-project
   ```

2. **Create a virtual environment**:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

4. **Run migrations**:
   ```
   python manage.py migrate
   ```

5. **Run the development server**:
   ```
   python manage.py runserver
   ```

## Usage

- Access the application at `http://127.0.0.1:8000/`.
- Use the Django admin interface to manage assets and portfolios.

## License

This project is licensed under the MIT License.