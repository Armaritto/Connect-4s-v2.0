document.addEventListener('DOMContentLoaded', () => {
    const setupElement = document.getElementById('setup');
    const gameElement = document.getElementById('game');
    const startButton = document.getElementById('start-button');
    const backButton = document.getElementById('back-button');
    const firstPlayerSelect = document.getElementById('first-player');
    const algorithmSelect = document.getElementById('algorithm');
    const boardElement = document.getElementById('board');
    const playerScoreElement = document.getElementById('player-score');
    const agentScoreElement = document.getElementById('agent-score');
    const traceElement = document.getElementById('trace');
    let board = Array(6).fill().map(() => Array(7).fill('E'));
    let currentPlayer = 'X';
    let selectedAlgorithm = 'random';

    startButton.addEventListener('click', async () => {
        currentPlayer = firstPlayerSelect.value;
        selectedAlgorithm = algorithmSelect.value;
        setupElement.style.display = 'none';
        gameElement.style.display = 'flex';
        renderBoard(board);

        if (currentPlayer === 'O') {
            await makeAgentMove();
        }
    });

    backButton.addEventListener('click', () => {
        gameElement.style.display = 'none';
        setupElement.style.display = 'flex';
        board = Array(6).fill().map(() => Array(7).fill('E'));
        renderBoard(board);
        playerScoreElement.textContent = '0';
        agentScoreElement.textContent = '0';
        traceElement.textContent = '';
    });

    function renderBoard(board) {
        boardElement.innerHTML = '';
        for (let rowIndex = 0; rowIndex < board.length; rowIndex++) {
            for (let colIndex = 0; colIndex < board[rowIndex].length; colIndex++) {
                const cellElement = document.createElement('div');
                cellElement.className = 'cell';
                if (board[rowIndex][colIndex] === 'X') {
                    cellElement.classList.add('red');
                } else if (board[rowIndex][colIndex] === 'O') {
                    cellElement.classList.add('yellow');
                }
                cellElement.dataset.column = colIndex;
                cellElement.addEventListener('click', handleCellClick);
                boardElement.appendChild(cellElement);
            }
        }
    }

    async function handleCellClick(event) {
        const column = event.target.dataset.column;
        try {
            const response = await fetch('http://127.0.0.1:5000/move', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ column: parseInt(column), board: board.map(row => row.join('')).join('\n'), algorithm: selectedAlgorithm })
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            board = data.board.split('\n').map(row => row.split(''));
            renderBoard(board);
            playerScoreElement.textContent = data.player_score;
            agentScoreElement.textContent = data.agent_score;
            traceElement.textContent = data.trace;
        } catch (error) {
            alert('Failed to connect to the server. Please try again later.');
        }
    }

    async function makeAgentMove() {
        try {
            const response = await fetch('http://127.0.0.1:5000/move', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ column: -1, board: board.map(row => row.join('')).join('\n'), algorithm: selectedAlgorithm })
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            board = data.board.split('\n').map(row => row.split(''));
            renderBoard(board);
            playerScoreElement.textContent = data.player_score;
            agentScoreElement.textContent = data.agent_score;
            traceElement.textContent = data.trace;
        } catch (error) {
            alert('Failed to connect to the server. Please try again later.');
        }
    }

    renderBoard(board);
});