document.addEventListener("DOMContentLoaded", () => {
    const videoElement = document.getElementById("camera-feed");
    const captureButton = document.getElementById("capture-button");
    const field = document.getElementById("field")

    // Get user media (camera) stream
    navigator.mediaDevices.getUserMedia({video: {
        facingMode: 'environment' // This selects the front camera
    }})
            .then((stream) => {
                videoElement.srcObject = stream;
            })
            .catch((error) => {
                console.error("Error accessing camera:", error);
            });

        // Handle the capture button click
        captureButton.addEventListener("click", () => {
            // Capture the current frame from the video stream
            field.textContent = "Processing...";
            const canvas = document.createElement("canvas");
            canvas.width = videoElement.videoWidth;
            canvas.height = videoElement.videoHeight;
            const context = canvas.getContext("2d");
            context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);

            // Convert the captured frame to a base64 encoded image
            const imageDataURL = canvas.toDataURL("image/jpeg");

            // Send the captured frame to the Flask server
            fetch("/process_frame", {
                method: "POST",
                body: JSON.stringify({ image_data: imageDataURL }),
                headers: {
                    "Content-Type": "application/json"
                }
            })
                .then((response) => response.json())
                .then((data) => {
                    // Redirect to the edited frame template
                    window.location.href = `/result/${data.filename}`;
                })
                .catch((error) => {
                    console.error("Error sending data to server:", error);
                });
        });
    });