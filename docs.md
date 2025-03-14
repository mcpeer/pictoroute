# Pictoroute

Pictoroute is a web application designed to process images of address tables, extract address information, and plan the shortest route between them. It leverages AI for image processing and geocoding to provide accurate and efficient route planning.

## Features

- **Image Upload**: Upload images containing address tables for processing.
- **Address Extraction**: Extracts and structures address information from images.
- **Geocoding**: Fetches coordinates for addresses.
- **Route Planning**: Calculates the shortest path between addresses.
- **Google Maps Integration**: Provides links for route navigation on Google Maps.

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd pictoroute
   ```

2. **Set up the environment**:
   - Copy the `.env.template` to `.env` and fill in the necessary environment variables.

3. **Install dependencies**:
   - For the backend, use Poetry:
     ```bash
     poetry install
     ```
   - For the frontend, navigate to the `frontend` directory and use npm:
     ```bash
     cd frontend
     npm install
     ```

4. **Build and run the Docker container**:
   ```bash
   ./build_and_run_dockerfile.sh
   ```

## Usage

- **Frontend**: Access the web application via your browser at `http://localhost:3000`.
- **Backend**: The API is available at `http://localhost:8000`.

## Testing

- Run tests for the backend using:
  ```bash
  poetry run pytest
  ```
- Run tests for the frontend using:
  ```bash
  cd frontend
  npm test
  ```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## Personal Note

This project was inspired by the needs of bike couriers who often have to visit multiple addresses in a day. The goal is to allow couriers to simply take a picture of their job list and automatically receive the shortest route to complete their deliveries efficiently. Currently, the start and end addresses are hardcoded in the code, and future improvements aim to generalize this feature to allow dynamic input.

## License

This project is licensed under the MIT License.
