({
    /**
     * @description: Close and redirect the modal
     */
    handleCloseModal: function(component) {
        let navEvt = this.constructNavigationEvent(
            component.get('v.parentId'),
            component.get('v.recordId')
        );

        component.get('v.modal').then(modal => {
            modal.close();
        });

        navEvt.fire();
    },

    /**
     * @description: Determine where the page should be redirect and construct the event
     */
    constructNavigationEvent: function(parentId, recordId) {
        let navEvt;

        if(parentId || recordId) {
            navEvt = $A.get("e.force:navigateToSObject");
            navEvt.setParams({
            "recordId": parentId || recordId,
            "slideDevName": "related"
            });

        } else {
            navEvt = $A.get("e.force:navigateToObjectHome");
            navEvt.setParams({
                "scope": "npe03__Recurring_Donation__c"
            });
        }

        return navEvt;
    },

    /**
    * @description: Extract and decode the Base64 component fragment from the URL to get the parent Id.
    * If the target fragment is not found, return a blank string or null.
    * @variable syntax A hardcoded text that is present in the URL when clicking 'New' button from Related List
    * @variable regex This regex expression targets the specific base64 encoded parameter in the URL.
    * @variable encodedParameters Extract out the target base64 encoded fragment. The regex should return 3 parts of parameters
    *   (with syntax, with '=1.', and pure base64 encoded fragment). The third part is the pure based64 encoded fragment
    * @variable decodedFragment Replace any '+' sign since it's replaced from space in URL
    *   and using the standard decodeURIComponent() function to decode the component
    * @return ParentId using wubdiw.atob() to convert the base64 string.
    * 
    */
    getParentId: function() {
        try {
            let syntax = 'inContextOfRef';
            syntax = syntax.replace(/[\[\]]/g, "\\$&");
            var url = window.location.href;
            var regex = new RegExp("[?&]" + syntax + "(=1\.([^&#]*)|&|#|$)");
            var encodedParameters = regex.exec(url);

            if (!encodedParameters) {
                return null;
            } else if (!encodedParameters[2]) {
                return '';
            }
            
            const decodedFragment = decodeURIComponent(encodedParameters[2].replace(/\+/g, " "));
            return JSON.parse(window.atob(decodedFragment)).attributes.recordId;

        } catch(error) {

        }
    }
})