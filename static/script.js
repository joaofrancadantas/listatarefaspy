async function enviarTarefa(tarefa) {
    try {

        const resposta = fetch(`/criar-tarefa/${tarefa}`, {
            method: 'POST',
            headers: {
                'content-type': 'application/json',
                'Accept': 'application/json'
            },
            body: {
                'tarefa': tarefa
            }
        })

        // if (!resposta.ok) throw new Error('Erro ao cadastrar');
    }

    catch(e) {
        console.log(e)
    }
}

async function carregarTarefas() {
    try {
        const resposta = await fetch ('/lista-tarefas',{
            method: 'GET'
        });

        if (resposta.ok) {
            const dados = await resposta.json();
            listarTarefas(dados)
            
        }
        if (!resposta.ok) throw new Error('Erro ao carregar');
    }
    catch (e) {
        console.log(e)
    }
}

 function listarTarefas(dados){
        const conteudo  = document.querySelector('.tarefaExistente');

        conteudo.innerHTML = dados.map(d => `<div class="tarefaListada" data-id="${d._id}"><span>${d.tarefa}</span><i class="fa-solid fa-trash lixeira" data-id="${d._id}" title="Excluir"></i></div>`).join('')
}


document.addEventListener('click', async (e) => {
    const botao = e.target.closest('.lixeira');

    if(!botao) return;

    const idTarefa = botao.dataset.id;

    try {
        const resp = await fetch(`/deletar/${idTarefa}`, {
            method: 'POST'
        });
        if (!resp.ok) throw new Error('Erro ao excluir');

        botao.closest('.tarefaListada').remove()
    } catch(e){
        alert("Erro ao excluir", e)
    }
})


document.addEventListener('DOMContentLoaded', carregarTarefas)

document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('input-tarefa')
    const form = document.getElementById('form-tarefa')

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const nomeTarefa = input.value.trim();

        if(!nomeTarefa) return;

        try {
            await enviarTarefa(nomeTarefa);
            input.value = '';
            await carregarTarefas();
        } catch(e){
            alert('Falha ao cadastrar tarefa!')
        }
    })
})