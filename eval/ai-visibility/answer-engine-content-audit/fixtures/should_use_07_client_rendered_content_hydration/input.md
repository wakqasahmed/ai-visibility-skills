# Input
Review content for `https://cloudapp.example/features`.
Target question: What features does CloudApp support?
Raw HTML inspection (`curl -s https://cloudapp.example/features`) returns `<div id="root"></div>` with empty text, but client-side JavaScript renders feature breakdown headings and text in the browser.
