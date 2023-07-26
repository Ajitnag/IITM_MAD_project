from website import create_app

# To run flask webserver
if __name__ == "__main__":

    app = create_app()
    app.run(debug=True)
