# Pictoroute

This project was inspired by the needs of bike couriers who often have to visit multiple addresses in a day. The goal is to allow couriers to simply take a picture of their job list and automatically receive the shortest route to complete their deliveries efficiently. Currently, the start and end addresses are hardcoded in the code, and future improvements aim to generalize this feature to allow dynamic start and end addresses.                                                                                                                                           

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

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## Screenshots

Below are the three main screens of the Pictoroute application, given the `input` as shown in `repo-assets/input.png`:

<p align="center">
  <img src="/repo-assets/screen1.png" alt="Screen 1" width="30%" />
  <img src="/repo-assets/screen2.png" alt="Screen 2" width="30%" />
  <img src="/repo-assets/screen3.png" alt="Screen 3" width="30%" />
</p>

The result of processing (the google maps route) can be found [here](https://www.google.com/maps/dir/Eemplein+65,+3812+EA+Amersfoort/Albert+Heijn+Amsterdamseweg/Albert+Heijn/Albert+Heijn+to+go/AH+Leusderweg/AH+Euterpeplein/AH+Buma,+Buma+1,+3825+ME+Amersfoort/AH+Albert+Schweitzersingel/Eemplein+65,+3812+EA+Amersfoort/@52.1715438,5.3559861,13z/data=!3m2!4b1!5s0x47c64402a5bd2199:0x93ba42dec49676dc!4m56!4m55!1m5!1m1!1s0x47c646a3fd81ec3b:0x275510101dabc7ac!2m2!1d5.3824825!2d52.1592796!1m5!1m1!1s0x47c6478a0b3f7007:0x90353441c7b4a208!2m2!1d5.3664494!2d52.1643202!1m5!1m1!1s0x47c646ac0b0f48af:0xdc677d8b4f8c9988!2m2!1d5.3666035!2d52.159882!1m5!1m1!1s0x47c646a7ed9d82c1:0xd36c797613274c9!2m2!1d5.374167!2d52.1543456!1m5!1m1!1s0x47c64419ec6c924f:0xa707b4ce9ab771a8!2m2!1d5.3805231!2d52.1439195!1m5!1m1!1s0x47c64429f21c6f29:0xee2fa550c64a6ce9!2m2!1d5.4055594!2d52.151536!1m5!1m1!1s0x47c647acefbed547:0xd5de12913da1a475!2m2!1d5.4305422!2d52.1961488!1m5!1m1!1s0x47c646ed83354723:0x482453524df4db95!2m2!1d5.4038817!2d52.17685!1m5!1m1!1s0x47c646a3fd81ec3b:0x275510101dabc7ac!2m2!1d5.3824825!2d52.1592796!3e1?entry=ttu&g_ep=EgoyMDI1MDMxMS4wIKXMDSoASAFQAw%3D%3D).

## License

This project is licensed under the MIT License.
