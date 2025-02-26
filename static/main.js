async function Hp(url,id){
    const input = document.getElementById("userInput").value;
    try {
        const response = await fetch(url, {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ "hp":input,"id":id }),
        });
        location.reload();
    } catch (error) {
        alert("Щось не те")
        console.error('Помилка:', error);
    }
}

function HpAdd(id){
    Hp('/hpAdd',id)
}
function HpSubtract(id){
    Hp('/hpSubtract',id)
}