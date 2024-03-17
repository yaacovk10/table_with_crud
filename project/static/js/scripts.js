import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
toast.configure();


//const MY_SERVER = 'https://librarymanag.netlify.app/customers'
const MY_SERVER = 'https://library-3xpb.onrender.com'
//const MY_SERVER = 'http://127.0.0.1:5000/customers';
const customerList = document.getElementById('customer-list');
const addCustomerButton = document.getElementById('add-customer');

// Function to show a success toast message
function showToastSuccess(message) {
    toast.success(message, {
        position: toast.POSITION.TOP_RIGHT,
    });
}

// Function to show an error toast message
function showToastError(message) {
    toast.error(message, {
        position: toast.POSITION.TOP_RIGHT,
    });
}

// Function to get customer data
const getCustomerData = async () => {
    try {
        const res = await axios.get(`${MY_SERVER}/get`);
        customerList.innerHTML = res.data.map(customer => `
            <tr>
                <td>${customer.id}</td>
                <td>${customer.first_name}</td>
                <td>${customer.last_name}</td>
                <td>${customer.city}</td>
                <td>${customer.age}</td>
                <td>
                    <button class='btn btn-danger' onClick='deleteCustomer(${customer.id})'>Delete</button>
                    <button class='btn btn-info' onClick='editCustomer(${customer.id})'>Edit</button>
                </td>
            </tr>`
        ).join('');
        showToastSuccess('Customer data loaded successfully');
    } catch (error) {
        showToastError('Error loading customer data');
        console.error(error);
    }
};

// Add event listener to the "Add Customer" button
addCustomerButton.addEventListener('click', () => addCustomer());

// Function to add a customer
const addCustomer = async () => {
    const id = document.getElementById('cust_id').value;
    const firstName = document.getElementById('first_name').value;
    const lastName = document.getElementById('last_name').value;
    const city = document.getElementById('cust_city').value;
    const age = document.getElementById('cust_age').value;

    try {
        await axios.post(`${MY_SERVER}/add`, {
            cust_id: id,
            first_name: firstName,
            last_name: lastName,
            cust_city: city,
            cust_age: age,
        });
        clearFields();
        getCustomerData();
        showToastSuccess('Customer added successfully');
    } catch (error) {
        showToastError('Error adding customer');
        console.error(error);
    }
};
// Function to delete a customer
async function del_cust(id) {
    try {
        await axios.delete(`${MY_SERVER}/${id}`);
        showToastSuccess('Customer deleted successfully');
        get_data();
    } catch (error) {
        showToastError('Error deleting customer');
    }
}

// Function to update a customer
async function upd_cust(id) {
    try {
        await axios.put(`${MY_SERVER}/${id}`, {
            "name": cust_name.value,
            "city": cust_city.value,
            "addr": cust_address.value
        });
        showToastSuccess('Customer updated successfully');
        get_data();
    } catch (error) {
        showToastError('Error updating customer');
    }
}

// Function to clear input fields
function clearFields() {
    const inputFields = ['cust_id', 'first_name', 'last_name', 'cust_city', 'cust_age'];
    inputFields.forEach(field => (document.getElementById(field).value = ''));
}

getCustomerData();
