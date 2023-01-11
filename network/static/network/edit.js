
const editBtn = document.querySelectorAll('.editBtn');

editBtn.forEach(button => {
    button.addEventListener('click', editPost);
})

function editPost() {
    this.disabled = "true";
    const postID = this.getAttribute('data-id');
    const post_text = document.querySelector(`#post-${postID} .post_text`);
    const postValue = post_text.innerText;
    post_text.innerHTML = `<br/><textarea class="edit-area">${postValue}</textarea>`;
    const saveBtn = document.createElement("button");
    saveBtn.id = `${postID}`;
    saveBtn.classList.add('btn');
    saveBtn.classList.add('btn-primary');
    saveBtn.innerText = 'Save';
    saveBtn.addEventListener('click', savePost)
    post_text.append(saveBtn);
}

function savePost() {
    const content = document.querySelector(`#post-${this.id} .edit-area`).value;
    const editBtn = document.getElementById(`editBtn_${this.id}`);
    fetch(`/edit/${this.id}`, {
        method: 'POST',
        body: JSON.stringify(content)
    })
        .then(response => response.json())
        .then(result => {
            console.log(result)
            document.querySelector(`#post-${this.id} .post_text`).innerHTML = content;

        })
    editBtn.disabled = false;
}