function GameSession() {
    this.coins = 0
    this.click_power = 1
    this.auto_click_power = 0
    this.next_level_price = 10
 
    this.init = function() {
        getCore().then(core => {
            this.coins = core.coins
            this.click_power = core.click_power
            this.auto_click_power = core.auto_click_power
            render()
        })
    }
    this.add_coins = function(coins) {
        this.coins += coins      
        updateCoins(this.coins)
        render()
    }
    this.add_power = function(power) {
        this.click_power += power
        render()
    }
    this.add_auto_power = function(power) {
        this.auto_click_power += power
        render()
    }
}

let Game = new GameSession() 

function call_click() {
    Game.add_coins(Game.click_power)    
}


/** Функция для обновления количества монет, 
 * невероятной мощи и дружинных кликуш в HTML-элементах. */
function render() {
    const coinsNode = document.getElementById('coins')
    const clickNode = document.getElementById('click_power')
    const autoClickNode = document.getElementById('auto_click_power')

    coinsNode.innerHTML = Game.coins
    clickNode.innerHTML = Game.click_power
    autoClickNode.innerHTML = Game.auto_click_power
}

/** Функция для обновления буста на фронтике. */
function update_boost(boost) {
    const boost_node = document.getElementById(`boost_${boost.id}`)
    boost_node.querySelector('#boost_level').innerText = boost.level
    boost_node.querySelector('#boost_power').innerText = boost.power
    boost_node.querySelector('#boost_price').innerText = boost.price    
}

/** Функция для добавления буста на фронтике. */
function add_boost(parent, boost) {
    const button = document.createElement('button')
    button.setAttribute('class', `boost_${boost.type}`)
    button.setAttribute('id', `boost_${boost.id}`)
    button.setAttribute('onclick', `buy_boost(${boost.id})`)
    button.innerHTML = `
        <p>lvl: <span id="boost_level">${boost.level}</span></p>
        <p>+<span id="boost_power">${boost.power}</span></p>

        <p><span id="boost_name">${boost.name}</span></p>
        <p><span id="boost_describtion">${boost.describtion}</span></p>

        <p><span id="boost_price">${boost.price}</span></p>
    `
    parent.appendChild(button)
}

/** Функция получения данных об игре пользователя с бэкенда. */
function getCore() {
    return fetch('/core/', {
        method: 'GET'
    }).then(response => {
        if (response.ok) {
            return response.json()
        }
        return Promise.reject(response) 
    }).then(response => {
        return response.core
    }).catch(error => console.log(error))
}

/** Функция отправки данных о количестве монет пользователя на бэкенд. */
function updateCoins(current_coins) {
    const csrftoken = getCookie('csrftoken')
    return fetch('/update_coins/', {
        method: 'POST',
        headers: {
            "X-CSRFToken": csrftoken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            current_coins: current_coins
        })
    }).then(response => {
        if (response.ok) {
            return response.json()
        }
        return Promise.reject(response)
    }).then(response => {
        if (response.is_levelup) {
            get_boosts()
        }
        return response.core
    }).catch(error => console.log(error))
}

/** Функция получения имеющихся бустов пользователя с бэкенда. */
function get_boosts() {
    return fetch('/boosts/', {
        method: 'GET'
    }).then(response => {
        if (response.ok) {
            return response.json()
        }
        return Promise.reject(response)
    }).then(boosts => {
        const panel = document.getElementById('boosts-holder')
        panel.innerHTML = ''
        boosts.forEach(boost => {
            add_boost(panel, boost)
        })
    }).catch(error => console.log(error))
}

/** Функция покупки буста. */
function buy_boost(boost_id) {
    const csrftoken = getCookie('csrftoken')
    return fetch(`/boost/${boost_id}/`, {
        method: 'PUT',
        headers: {
            "X-CSRFToken": csrftoken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            coins: Game.coins
        })
    }).then(response => {
        if (response.ok) return response.json()
        return Promise.reject(response)
    }).then(response => {
        if (response.error) return
        const old_boost_stats = response.old_boost_stats
        const new_boost_stats = response.new_boost_stats
       
        Game.add_coins(-old_boost_stats.price)
        if (old_boost_stats.type === 1) {
            Game.add_auto_power(old_boost_stats.power)
        } else {
            Game.add_power(old_boost_stats.power)
        }
        update_boost(new_boost_stats) // Обновляем буст на фронтике.
    }).catch(err => console.log(err))
}

/** Функция обработки автоматического клика. */
function setAutoClick() {
    setInterval(function() {
        Game.add_coins(Game.auto_click_power)
        updateCoins(Game.coins)
    }, 1000)
}

/** Функция обработки автоматического сохранения (отправки данных о количестве монет пользователя на бэкенд). */
function setAutoSave() {
    setInterval(function() {
        updateCoins(Game.coins)
    }, 60000)
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

window.onload = function () {
    Game.init() // Инициализация игры.
    setAutoClick() // Инициализация автоклика.
    setAutoSave() // Инициализация автосейва.
}

/**function call_click() {    
    fetch('/call_click/', {
        method: 'GET'
    }).then(response => {
        if (response.ok) {
            return response.json()
        }
        return Promise.reject(response)
    }).then(data => {
        document.getElementById('coins').innerText = data.core.coins
        if (data.is_levelup) {
            get_boosts()
        }
    }).catch(error => console.log(error))    
}
*/

