import Toybox.System;
import Toybox.Communications;
import Toybox.Lang;

class CommsRequest {

    function defaultCallback() as Void {
        // Default implementation
    }

    var priceCallback as Method = method(:defaultCallback);

    public var euros as Number = -1;
    public var cents as Number = -1;

    public var lastReqCode as Number = -1;

    public var lastResponse as String = "";

    // set up the response callback function
    function onReceive(responseCode as Number, data as String) as Void {
        if (responseCode == 200) {
            System.println("Request Successful");                   // print success

            // massive html, find the index of "€" symbol in the text
            var index = data.find("€");

            // get the substring from the index of "€" to the end of the text
            var substring = data.substring(index, data.length());

            // find the index of the first "<" symbol in the substring
            var endIndex = substring.find("<");
            
            // get the substring from the beginning of the substring to the index of "<"
            var rawPrice = substring.substring(0, endIndex);

            var euroCount = rawPrice.substring(rawPrice.find(" ") + 1, rawPrice.find(",")).toNumber();
            var centCount = rawPrice.substring(rawPrice.find(",") + 1, rawPrice.length()).toNumber();

            euros = euroCount;
            cents = centCount;

            priceCallback.invoke();
        } else {
            System.println("Response: " + responseCode);            // print response code
            euros = -1;                                              // set euros to -1
            cents = -1;                                              // set cents to -1
            priceCallback.invoke();                           // invoke the callback with -1, -1
        }

        lastResponse = data;
        lastReqCode = responseCode;
    }

    function makeRequest(callback as Method) as Void {
        var url = "https://mijnkniponline.nl/s/";

        var params = {                                              // set the parameters
            
        };

        var options = {                                             // set the options
            :method => Communications.HTTP_REQUEST_METHOD_GET,      // set HTTP method
            :headers => {                                           // set headers
            "Content-Type" => Communications.REQUEST_CONTENT_TYPE_JSON},
            // set response type
            :responseType => Communications.HTTP_RESPONSE_CONTENT_TYPE_TEXT_PLAIN
        };

        var responseCallback = method(:onReceive);                  // set responseCallback 
        
        
        //save the callback passed in to object
        priceCallback = callback;

        // onReceive() method
        // Make the Communications.makeWebRequest() call
        Communications.makeWebRequest(url, params, options, method(:onReceive));
    }
}