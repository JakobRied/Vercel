from flask import Flask, render_template, send_from_directory, jsonify, request, Response
import cv2, os, base64, sys

sys.path.append("D:\Desktop\Alles\Informatik\\taxinumberapp\web_camera")
from yolo_number import detect_number, extract_number
from portal_request import verification_request
 

app = Flask(__name__) 
app.secret_key = "abc" #Secret Key

number = 0
state = "unset"

@app.route("/")
def index():
    return render_template("mobileIndex.html")

@app.route("/report")
def report():
    return render_template("report.html")

@app.route('/process_frame', methods=['POST'])
def process_frame():
    global filename
    try:
        data = request.get_json()
        image_data = data.get('image_data', '')

        # Decode base64 image data
        image_data = image_data.split(',')[1]
        image_binary = base64.b64decode(image_data)

        
        # Save the image temporarily (you may want to use a proper storage solution)
        filename = 'captured_frame.jpg'
        with open(os.path.join("static", filename), 'wb') as f:
            f.write(image_binary)

        # Perform your image processing here (edit the image)
        

        # Return the filename of the edited image
        return jsonify({'filename': filename})

       # return jsonify({'filename': filename})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/result/<filename>')
def result(filename):
    print(filename)
    img = cv2.imread("static\\captured_frame.jpg")

    if img is None or img.size == 0:
        return render_template("failed.html", error="Couldn't load image with cv2", filename=filename)

    try: #predict Yolo on image
        img_cropped, img_boxed = detect_number(img, offset=3)
    except TypeError: #failed
        return render_template("failed.html", error="Problem with loading image for detection", filename=filename)
    
   # cv2.imshow("image", img_cropped)
    #cv2.imshow("image", img_boxed)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    if img_cropped is None: #no Taxi detected
        return render_template("failed.html", error="No taxi could be detected in the image", filename=filename)

    
    filenameEdited = "captured_frame_edited.jpg"
    with open("static\\captured_frame_edited.jpg", 'wb') as f:
        f.write(img_boxed)
    
    number = extract_number(img_cropped, psm=13)
    if number is None:
        return render_template("failed.html", error="No Taxi-Number-Format could be detected in the image", filename=filenameEdited)

    valid = verification_request(number)
    if valid:
        return render_template("mobile-valid.html", number=number)
    
    return render_template("mobile-invalid.html", filename=filenameEdited, number=number)
    
if __name__=="__main__":
    context = ('cert.pem', 'key.pem') #Location of certificate & key
    app.run(port=5000, ssl_context=context, host='0.0.0.0', debug=True) #Specify variable to run function