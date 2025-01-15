
// Function to fetch prayer times for a given city from the Flask API
function fetchPrayerTimes() {
    const city = document.getElementById('city').value.trim();

    if (!city) {
        alert("Please enter a city name.");
        return;
    }

    fetch(`/get_prayer_times?city=${city}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById('prayer-times').innerHTML = `<p>Error: ${data.error}</p>`;
            } else {
                const timings = data;
                let prayerTimesHtml = `
                    <ul>
                        <li><strong>Fajr:</strong> ${timings.Fajr}</li>
                        <li><strong>Dhuhr:</strong> ${timings.Dhuhr}</li>
                        <li><strong>Asr:</strong> ${timings.Asr}</li>
                        <li><strong>Maghrib:</strong> ${timings.Maghrib}</li>
                        <li><strong>Isha:</strong> ${timings.Isha}</li>
                    </ul>
                `;
                document.getElementById('prayer-times').innerHTML = prayerTimesHtml;
            }
        })
        .catch(error => {
            document.getElementById('prayer-times').innerHTML = `<p>There was an error fetching the data. Please try again later.</p>`;
        });
}
