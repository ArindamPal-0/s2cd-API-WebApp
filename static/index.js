document.addEventListener('DOMContentLoaded', event => {
    console.log('s2cd frontend');

    autoRefreshButton = document.querySelector('#auto_refresh');
    // console.log(autoRefreshButton);
    refreshButton = document.querySelector('#refresh');
    // console.log(refreshButton);

    autoRefreshButton.addEventListener('click', event => {
        // console.log(autoRefreshButton.checked);
        if(autoRefreshButton.checked) {
            refreshButton.classList.add('display-none');
        }
        else {
            refreshButton.classList.remove('display-none');
        }
    });

    tbody = document.querySelector('tbody');
    // console.log(tbody);

    apiUrl = '/api/sensor_values'
    
    fetch(apiUrl)
    .then(response => response.json())
    .then(data => {
        // console.log('success', data);
        while(tbody.firstChild){
            tbody.firstChild.remove();
        }

        let array = data['data'];
        for(let i = 0; i < array.length; i++) {
            let tr = document.createElement('tr');
    
            let tdSno = document.createElement('td');
            tdSno.textContent = `${i + 1}`;
            let tdValue = document.createElement('td');
            tdValue.textContent = `${array[i]['sensor value']}`;
            let tdDate = document.createElement('td');
            tdDate.textContent = `${array[i]['date added']}`
    
            tr.appendChild(tdSno);
            tr.appendChild(tdValue);
            tr.appendChild(tdDate);
    
            tbody.appendChild(tr);
        }
    })
    .catch(err => console.error('Error:', err));

    refreshButton.addEventListener('click', event => {
        fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            // console.log('success', data);
            while(tbody.firstChild){
                tbody.firstChild.remove();
            }

            let array = data['data'];
            for(let i = 0; i < array.length; i++) {
                let tr = document.createElement('tr');
        
                let tdSno = document.createElement('td');
                tdSno.textContent = `${i + 1}`;
                let tdValue = document.createElement('td');
                tdValue.textContent = `${array[i]['sensor value']}`;
                let tdDate = document.createElement('td');
                tdDate.textContent = `${array[i]['date added']}`
        
                tr.appendChild(tdSno);
                tr.appendChild(tdValue);
                tr.appendChild(tdDate);
        
                tbody.appendChild(tr);
            }
        })
        .catch(err => console.error('Error:', err));
    });
    
    setInterval(() => {
        if(document.hasFocus()) {
            if(autoRefreshButton.checked) {
                fetch(apiUrl)
                .then(response => response.json())
                .then(data => {
                    while(tbody.firstChild) {
                        tbody.firstChild.remove();
                    }
                    // tbody.innerHTML = '';
    
                    // console.log('success', data);
                    let array = data['data'];
                    for(let i = 0; i < array.length; i++) {
                        let tr = document.createElement('tr');
                
                        let tdSno = document.createElement('td');
                        tdSno.textContent = `${i + 1}`;
                        let tdValue = document.createElement('td');
                        tdValue.textContent = `${array[i]['sensor value']}`;
                        let tdDate = document.createElement('td');
                        tdDate.textContent = `${array[i]['date added']}`
                
                        tr.appendChild(tdSno);
                        tr.appendChild(tdValue);
                        tr.appendChild(tdDate);
                
                        tbody.appendChild(tr);
                    }
                })
                .catch(err => console.error('Error:', err));
            }
        }
    }, 2000);
})