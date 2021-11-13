document.addEventListener('DOMContentLoaded', event => {
    console.log('s2cd frontend');

    tbody = document.querySelector('tbody');
    // console.log(tbody);

    apiUrl = '/api/sensor_values'
    
    
    setInterval(() => {
        if(document.hasFocus()) {
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

    }, 2000);
})