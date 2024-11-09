import Toybox.Graphics;
import Toybox.WatchUi;
import Toybox.System;
import Toybox.Lang;
import Toybox.Communications;

class SchoolFaceView extends WatchUi.View {

    var comms as CommsRequest = new CommsRequest();

    var nUpdated as Number = 0;

    function initialize() {
        View.initialize();
    }

    // Load your resources here
    function onLayout(dc as Dc) as Void {
        setLayout(Rez.Layouts.MainLayout(dc));
        loadData();
    }

    // Called when this View is brought to the foreground. Restore
    // the state of this View and prepare it to be shown. This includes
    // loading resources into memory.
    function onShow() as Void {
        //update
        comms.makeRequest(
            method(:priceCallback)
        );
    }

    function priceCallback() as Void {
        var centText = comms.cents.toString();

        if (comms.cents < 10) {
            centText = "0" + centText;

            System.println("text: " + centText);
        }

        System.println("Price got: €" + comms.euros + "." + centText);

        // Update the view
        WatchUi.requestUpdate();
    }

    function loadData() as Void {
        comms.makeRequest(
            method(:priceCallback)
        );
    }

    // Update the view
    function onUpdate(dc as Dc) as Void {
        // Call the parent onUpdate function to redraw the layout
        View.onUpdate(dc);

        // Get label
        var priceLabel = View.findDrawableById("priceLabel") as Text;

        nUpdated = nUpdated + 1;

        if (comms.euros != -1) {
            // Set text
            priceLabel.setText("€ " + comms.euros + "." + comms.cents);
        } else { 
            System.println("Error in request!");

            // Set text
            priceLabel.setText("€ --.--");
        }

        var reponseLabel = View.findDrawableById("responsecode") as Text;

        reponseLabel.setText("(" + nUpdated + ", " + comms.lastReqCode + ")");
    }

    // Called when this View is removed from the screen. Save the
    // state of this View here. This includes freeing resources from
    // memory.
    function onHide() as Void {
        // Nothing to do here
    }

}
