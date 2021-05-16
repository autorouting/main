function googleTranslateElementInit() {
    new google.translate.TranslateElement({pageLanguage: 'en'}, 'google_translate_element');
}
            window.formbutton=window.formbutton||function(){(formbutton.q=formbutton.q||[]).push(arguments)};
formbutton("create", {
    action: "https://formspree.io/f/xdopqwzj",
    title: "Comments?", 
    description: "Send 'em in!",
    fields: [
    { 
        type: "email", 
        label: "Your Email (Optional):",
        name: "_replyto",
        required: false,
        placeholder: "joshswain@example.com"
    },
    {
        type: "textarea",
        label: "Message:",
        name: "message",
        required: true,
        placeholder: "I found a bug!",
    },
    { type: "submit" }      
    ],
    styles: {
        title: {
            backgroundColor: "#222222"
        },
        description: {
            backgroundColor: "#222222"
        },
        button: {
            backgroundColor: "#222222"
        }
    }
});