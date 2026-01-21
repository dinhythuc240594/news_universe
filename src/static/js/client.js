
UI_CLIENT = {

    SITE: localStorage.getItem('site') || 'vn',

    homeMainContent: function(){
        updateDateTime();
    },

    updateDateTime: function() {
        var now = new Date();
        var options = {
            weekday: 'long', 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        };

        options.locale = UI_CLIENT.SITE == 'vn'? 'vi-VN':'en-US';
        setInterval(function(){
            var dateTimeString = now.toLocaleDateString(options.locale, options);
            $('#current-date-time').text(dateTimeString);
        }, 60000);
    },

    formatTimeAgoFromIso: async function(dateStr) {
        if (!dateStr) return MyLang.getMsg('JUST_NOW');
        const date = new Date(dateStr);
        const now = new Date();
        const diffMs = now - date;
        const diffMinutes = Math.floor(diffMs / 60000);
        const diffHours = Math.floor(diffMinutes / 60);
        const diffDays = Math.floor(diffHours / 24);

        if (diffDays > 0) return diffDays + MyLang.getMsg('DAY_AGO');
        if (diffHours > 0) return diffHours + MyLang.getMsg('HOUR_AGO');
        if (diffMinutes > 0) return diffMinutes + MyLang.getMsg('MINUTE_AGO');
        return MyLang.getMsg('JUST_NOW');
    },

    validateEmail: function(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    },

    loadWeatherData: async function(){
        var weatherWidget = $('#weather-widget');
        if (!weatherWidget.length) return;
        fetch(`https://geocoding-api.open-meteo.com/v1/search?name=Saigon&count=1&language=${UI_CLIENT.SITE}&format=json`)
            .then(response => response.json())
            .then(data => {
                if (data.results && data.results.length > 0) {
                    const location = data.results[0];
                    const latitude = location.latitude;
                    const longitude = location.longitude;
                    const cityName = site == 'en' ? 'Ho Chi Minh City' : 'TP. Hồ Chí Minh';
                    
                    // Get current weather
                    return fetch(`https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m&timezone=Asia/Ho_Chi_Minh`)
                        .then(response => response.json())
                        .then(weatherData => {
                            displayWeather(cityName, weatherData);
                        });
                } else {
                    throw new Error('Không tìm thấy thành phố');
                }
            })
            .catch(error => {
                console.error('Weather API error:', error);
                // Fallback to wttr.in API
                loadWeatherFallback(city);
            });
    },

    loadWeatherFallback: async function(city){
        fetch(`https://wttr.in/${city}?format=j1&lang=vi`)
            .then(response => response.json())
            .then(data => {
                if (data.current_condition && data.current_condition[0]) {
                    const current = data.current_condition[0];
                    const location = data.nearest_area[0].areaName[0].value;
                    
                    const weatherData = {
                        current: {
                            temperature_2m: parseFloat(current.temp_C),
                            relative_humidity_2m: parseFloat(current.humidity),
                            wind_speed_10m: parseFloat(current.windspeedKmph) / 3.6, // Convert km/h to m/s
                            weather_code: getWeatherCode(current.weatherDesc[0].value)
                        }
                    };
                    
                    displayWeather(location, weatherData);
                } else {
                    throw new Error('Không thể lấy dữ liệu thời tiết');
                }
            })
            .catch(error => {
                console.error('Weather fallback error:', error);
                displayWeatherError();
            });
    },

    displayWeather: function name(cityName, weatherData) {
        const site = window.location.pathname.split('/')[1];
        const weatherWidget = $('#weather-widget');
        const current = weatherData.current;
        
        // Get weather icon and description
        const weatherInfo = getWeatherInfo(current.weather_code);
        const time = new Date(current.time);
        const hours = time.getHours();
        // const minutes = time.getMinutes();
        // const seconds = time.getSeconds();
        // const timeString = `${hours}:${minutes}:${seconds}`;

        if((hours > 6 && hours < 18) && (weatherInfo.icon == 'fas fa-sun' || weatherInfo.icon == 'fas fa-cloud-sun')) {
            weatherInfo.icon = 'fas fa-sun';
            weatherInfo.description = MyLang.getMsg('MSG_SUN');
        } else {
            if((hours > 18 && hours < 24) || (hours > 0 && hours < 6)) {
                weatherInfo.icon = 'fas fa-moon';
                weatherInfo.description = MyLang.getMsg('MSG_NIGHT');
            }
        }
        
        const temperature = Math.round(current.temperature_2m);
        const humidity = Math.round(current.relative_humidity_2m);
        const windSpeed = Math.round(current.wind_speed_10m * 3.6); // Convert m/s to km/h
        
        var html = '';
            html += '<div class="city-name">'+ cityName +'</div>';
            html += '<div class="temperature">'+ temperature + MyLang.getMsg('MSG_OPERATOR_TEMP') + '</div>';
            html += '<div class="weather-desc">';
            html += '<i class="'+ weatherInfo.icon +'"></i>' + weatherInfo.description;
            html += '</div>';
            html += '<div class="weather-details">';
            html += '<div class="detail-item">';
            html += '<i class="fas fa-tint"></i>';
            html += '<span>'+ MyLang.getMsg('MSG_HUMIDITY') + humidity +'%</span>';
            html += '</div>';
            html += '<div class="detail-item">';
            html += '<i class="fas fa-wind"></i>';
            html += '<span>'+ MyLang.getMsg('MSG_WINDY') + windSpeed +'km/h</span>';
            html += '</div>';
            html += '</div>';
        
        weatherWidget.html(weatherHTML);
    },

    // Get weather icon and description from weather code (WMO Weather interpretation codes)
    getWeatherInfo: function(code) {
        const weatherMap = {
            0: { icon: 'fas fa-sun', description: site == 'en' ? 'Sunny' : 'Trời nắng' },
            1: { icon: 'fas fa-sun', description: site == 'en' ? 'Sunny' : 'Trời quang' },
            2: { icon: 'fas fa-cloud-sun', description: site == 'en' ? 'Cloudy' : 'Ít mây' },
            3: { icon: 'fas fa-cloud', description: site == 'en' ? 'Cloudy' : 'Nhiều mây' },
            45: { icon: 'fas fa-smog', description: site == 'en' ? 'Fog' : 'Sương mù' },
            48: { icon: 'fas fa-smog', description: site == 'en' ? 'Fog' : 'Sương mù' },
            51: { icon: 'fas fa-cloud-rain', description: site == 'en' ? 'Rain' : 'Mưa nhẹ' },
            53: { icon: 'fas fa-cloud-rain', description: site == 'en' ? 'Rain' : 'Mưa vừa' },
            55: { icon: 'fas fa-cloud-rain', description: site == 'en' ? 'Rain' : 'Mưa nặng' },
            56: { icon: 'fas fa-cloud-rain', description: site == 'en' ? 'Rain' : 'Mưa đá nhẹ' },
            57: { icon: 'fas fa-cloud-rain', description: site == 'en' ? 'Rain' : 'Mưa đá nặng' },
            61: { icon: 'fas fa-cloud-showers-heavy', description: site == 'en' ? 'Rain' : 'Mưa nhẹ' },
            63: { icon: 'fas fa-cloud-showers-heavy', description: site == 'en' ? 'Rain' : 'Mưa vừa' },
            65: { icon: 'fas fa-cloud-showers-heavy', description: site == 'en' ? 'Rain' : 'Mưa nặng' },
            66: { icon: 'fas fa-cloud-rain', description: site == 'en' ? 'Rain' : 'Mưa đá nhẹ' },
            67: { icon: 'fas fa-cloud-rain', description: site == 'en' ? 'Rain' : 'Mưa đá nặng' },
            71: { icon: 'fas fa-snowflake', description: site == 'en' ? 'Snow' : 'Tuyết nhẹ' },
            73: { icon: 'fas fa-snowflake', description: site == 'en' ? 'Snow' : 'Tuyết vừa' },
            75: { icon: 'fas fa-snowflake', description: site == 'en' ? 'Snow' : 'Tuyết nặng' },
            77: { icon: 'fas fa-snowflake', description: site == 'en' ? 'Snow' : 'Hạt tuyết' },
            80: { icon: 'fas fa-cloud-showers-heavy', description: site == 'en' ? 'Rain' : 'Mưa rào nhẹ' },
            81: { icon: 'fas fa-cloud-showers-heavy', description: site == 'en' ? 'Rain' : 'Mưa rào vừa' },
            82: { icon: 'fas fa-cloud-showers-heavy', description: site == 'en' ? 'Rain' : 'Mưa rào nặng' },
            85: { icon: 'fas fa-snowflake', description: site == 'en' ? 'Snow' : 'Mưa tuyết nhẹ' },
            86: { icon: 'fas fa-snowflake', description: site == 'en' ? 'Snow' : 'Mưa tuyết nặng' },
            95: { icon: 'fas fa-bolt', description: site == 'en' ? 'Thunder' : 'Dông' },
            96: { icon: 'fas fa-bolt', description: site == 'en' ? 'Thunder' : 'Dông có mưa đá' },
            99: { icon: 'fas fa-bolt', description: site == 'en' ? 'Thunder' : 'Dông có mưa đá nặng' },
    };
    
    return weatherMap[code] || { icon: 'fas fa-cloud', description: site == 'en' ? 'Cloudy' : 'Nhiều mây' };
}

}