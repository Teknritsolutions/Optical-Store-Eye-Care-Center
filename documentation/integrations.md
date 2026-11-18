# Integration boundaries

No endpoint is connected by default. Booking, contact and newsletter submissions validate in the browser and return an explicitly labelled demo preview. Their data is not sent or saved. localStorage is used only for theme and direction preferences. No cookies or analytics are installed.

After `main.js` is loaded, attach an asynchronous adapter:

```js
window.OculisForms.booking = async function (fields) {
  const response = await fetch('/api/appointment-enquiries', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(fields)
  });
  if (!response.ok) throw new Error('Request failed');
  return { message: 'Your enquiry was received. The practice will confirm your appointment.' };
};
```

Use the same contract for `OculisForms.contact` and `OculisForms.newsletter`. Do not put secrets into client JavaScript. Adapters receive validated values, return a user-safe message, and may throw for failure. The submit button is disabled while an adapter is pending. Add appropriate server validation, spam controls, delivery handling and consent for your actual deployment.

Demo appointment times are not live inventory. Replace them with server-provided availability and validate date/time on the server. A request acknowledgement must not imply a confirmed appointment unless the booking backend actually confirms it. The demo avoids collecting medical history.

Replace `.demo-map` in contact.html with an accessible iframe or your map provider's component after verifying your store location. Provide a meaningful title, responsive dimensions and a text address alternative.

`sitemap.xml` uses https://oculis.example as a clearly fictional origin. Replace that origin and set the Sitemap directive in robots.txt to your real deployment URL. The shipped robots.txt blocks indexing to prevent accidental publication of fictional business content; change it deliberately when launching a verified production site.
