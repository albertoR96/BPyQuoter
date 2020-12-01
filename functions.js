function saveEntity(entity, elements) {
  let isNew = true;
  let params = '';
  let cnt = 1;
  for (const inpElm of elements) {
    if (inpElm.name != '' && (inpElm.tagName == 'INPUT' || inpElm.tagName == 'TEXTAREA')) {
      if (inpElm.name == 'id' && inpElm.value != '') {
        isNew = false;
        params += `${inpElm.name}=${encodeURI(inpElm.value)}&`;
      }
      if (cnt < elements.length - 1 && inpElm.name != 'id') {
        params += `${inpElm.name}=${encodeURI(inpElm.value)}&`;
      } else if (inpElm.name != 'id') {
        params += `${inpElm.name}=${encodeURI(inpElm.value)}`;
      }
    }
    cnt++;
  }
  let url = `http://localhost:8000/${entity}?action=${(isNew) ? 'new' : 'update'}&`;
  fetch(url + params).then(response => response.json()).then(data => (data.code == 1) ? alert('Informacion guardada') : alert('Al parecer hubo un error. Porfavor vuelva a intentarlo más tarde.'));
  for (const inpElm of elements) {
    inpElm.value = '';
  }
}

async function fetchData(entity) {
  const data = await fetch(`http://localhost:8000/${entity}`);
  return data.json();
}

async function getData() {
  return {
    articles: await fetchData('articles'),
    customers: await fetchData('customers'),
    suppliers: await fetchData('suppliers')
  }
}

function fillForm(idForm, data) {
  for (const prop in data) {
    if (data.hasOwnProperty(prop)) {
      $(`#${idForm} input[name="${prop}"], #${idForm} textarea[name="${prop}"]`).val(data[prop]);
    }
  }
}

function deleteEntity(entity, elements) {
  let isNew = true;
  let params = '';
  let cnt = 1;
  for (const inpElm of elements) {
    if (inpElm.name != '' && (inpElm.tagName == 'INPUT' || inpElm.tagName == 'TEXTAREA')) {
      if (inpElm.name == 'id' && inpElm.value != '') {
        isNew = false;
        params += `${inpElm.name}=${encodeURI(inpElm.value)}&`;
      }
      if (cnt < elements.length - 1 && inpElm.name != 'id') {
        params += `${inpElm.name}=${encodeURI(inpElm.value)}&`;
      } else if (inpElm.name != 'id') {
        params += `${inpElm.name}=${encodeURI(inpElm.value)}`;
      }
    }
    cnt++;
  }
  let url = `http://localhost:8000/${entity}?action=delete&`;
  fetch(url + params).then(response => response.json()).then(data => (data.code == 1) ? alert('Informacion guardada') : alert('Al parecer hubo un error. Porfavor vuelva a intentarlo más tarde.'));
}

$(document).ready(async () => {
  $('#saveArticleBtn').click(() => { saveEntity('articles', $('#articleForm input, #articleForm textarea').toArray()); });
  $('#saveCustomerBtn').click(() => { saveEntity('customers', $('#customerForm input').toArray()); });
  $('#saveSupplierBtn').click(() => { saveEntity('suppliers', $('#supplierForm input').toArray()); });
  $('#deleteArticleBtn').click(() => { deleteEntity('articles', $('#articleForm input, #articleForm textarea').toArray()); });
  $('#deleteCustomerBtn').click(() => { deleteEntity('customers', $('#customerForm input').toArray()); });
  $('#deleteSupplierBtn').click(() => { deletentity('suppliers', $('#supplierForm input').toArray()); });
  let data = await getData();
  $('#articles').DataTable({
    data: data.articles,
    columns: [
      { data: 'id'},
      { data: 'code'},
      { data: 'description'},
      { data: 'cost'}
    ],
    createdRow: (row, data, index) => {
      $(row).click(() => { fillForm('articleForm', data); });
    }
  });
  $('#customers').DataTable({
    data: data.customers,
    columns: [
      { data: 'id'},
      { data: 'name'},
      { data: 'branch'},
      { data: 'rfc'}
    ],
    createdRow: (row, data, index) => {
      $(row).click(() => { fillForm('customerForm', data); });
    }
  });
  $('#suppliers').DataTable({
    data: data.suppliers,
    columns: [
      { data: 'id'},
      { data: 'name'},
      { data: 'currency'},
      { data: 'category'}
    ],
    createdRow: (row, data, index) => {
      $(row).click(() => { fillForm('supplierForm', data); });
    }
  });
});