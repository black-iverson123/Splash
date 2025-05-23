var page = 1;
var total_count = 0;
var currentSort = 'rank';
var sortOrder = 'asc';

function fetchData() {
    $.ajax({
        url: '/main/coin-data',
        type: 'GET',
        data: {
            'page': page,
            'sort': currentSort,
            'order': sortOrder
        },
        success: function(data) {
            var coins_data = data.coins;
            total_count = data.total_count;

            var coinRows = '';
            coins_data.forEach(function(coin) {
                coinRows += `
                    <tr>
                        <td>${coin.rank}</td>
                        <td>${coin.name}</td>
                        <td>${coin.symbol}</td>
                        <td>${coin.price}</td>
                        <td>${coin.circulating_supply} ${coin.symbol}</td>
                        <td>${coin.volume_24h}</td>
                        <td>
                            <div class="progress-bar ${coin.percent_change_in_1h < 0 ? 'negative' : 'positive'}">
                                <span style="width: ${Math.abs(coin.percent_change_in_1h)}%;">
                                    ${coin.percent_change_in_1h < 0 ? '▼' : '▲'} ${coin.percent_change_in_1h}%
                                </span>
                            </div>
                        </td>
                        <td>
                            <div class="progress-bar ${coin.percent_change_in_24h < 0 ? 'negative' : 'positive'}">
                                <span style="width: ${Math.abs(coin.percent_change_in_24h)}%;">
                                    ${coin.percent_change_in_24h < 0 ? '▼' : '▲'} ${coin.percent_change_in_24h}%
                                </span>
                            </div>
                        </td>
                        <td>
                            <div class="progress-bar ${coin.percent_change_in_7d < 0 ? 'negative' : 'positive'}">
                                <span style="width: ${Math.abs(coin.percent_change_in_7d)}%;">
                                    ${coin.percent_change_in_7d < 0 ? '▼' : '▲'} ${coin.percent_change_in_7d}%
                                </span>
                            </div>
                        </td>
                    </tr>
                `;
            });


            $('#coin-data-body').html(coinRows);

            document.getElementById('prev-page').disabled = page <= 1;
            document.getElementById('next-page').disabled = page >= (total_count / 50);

            document.getElementById('current-page').textContent = `Page ${page}`;
        },
        error: function(error) {
            console.log('Error fetching data:', error);
        }
    });
}

function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    document.querySelector('.coins-container').classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode') ? 'enabled' : 'disabled');
}

window.onload = function() {
    fetchData();
    setInterval(fetchData, 5000);

    document.getElementById('prev-page').addEventListener('click', function() {
        if (page > 1) {
            page--;
            fetchData();
        }
    });

    document.getElementById('next-page').addEventListener('click', function() {
        if (page <= (total_count / 50)) {
            page++;
            fetchData();
        }
    });

    document.querySelectorAll('th.sortable').forEach(function(header) {
        header.addEventListener('click', function() {
            const sort = this.getAttribute('data-sort');
            if (currentSort === sort) {
                sortOrder = sortOrder === 'asc' ? 'desc' : 'asc';
            } else {
                currentSort = sort;
                sortOrder = 'asc';
            }
            fetchData();
        });
    });

    document.getElementById('search-input').addEventListener('input', function() {
        const query = this.value.toLowerCase();
        document.querySelectorAll('#coin-data-body tr').forEach(function(row) {
            const name = row.cells[1].textContent.toLowerCase();
            row.style.display = name.includes(query) ? '' : 'none';
        });
    });

    document.getElementById('dark-mode-toggle').addEventListener('click', toggleDarkMode);

    if (localStorage.getItem('darkMode') === 'enabled') {
        document.body.classList.add('dark-mode');
        document.querySelector('.coins-container').classList.add('dark-mode');
    }
};