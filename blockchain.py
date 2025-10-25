from flask import Flask, request, render_template_string, jsonify
import time
import hashlib
import json

# -------------------------
# Initialize Flask App
# -------------------------
app = Flask(__name__)

# -------------------------
# Blockchain Class
# -------------------------
class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.create_block(proof=100, previous_hash='1')  # Genesis block

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'agreements': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    def add_transaction(self, party_a, party_b, agreement_title, terms, date_signed):
        self.current_transactions.append({
            'party_a': party_a,
            'party_b': party_b,
            'agreement_title': agreement_title,
            'terms': terms,
            'date_signed': date_signed
        })
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        encoded = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f"{last_proof}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

# -------------------------
# Initialize Blockchain
# -------------------------
blockchain = Blockchain()

# -------------------------
# HTML Template
# -------------------------
template = '''
<!DOCTYPE html>
<html>
<head>
    <title>📜 Blockchain Legal Agreement System</title>
    <style>
        body { font-family: Arial; background: #f4f4f4; padding: 40px; }
        form { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); max-width: 600px; margin-bottom: 40px; }
        input, textarea, button { padding: 10px; width: 100%; margin-top: 10px; }
        button { background: #007bff; color: white; border: none; cursor: pointer; border-radius: 4px; }
        .block { background: white; padding: 15px; margin-bottom: 10px; border-left: 5px solid #007bff; box-shadow: 0 1px 5px rgba(0,0,0,0.1); border-radius: 4px; }
        pre { white-space: pre-wrap; word-wrap: break-word; }
    </style>
</head>
<body>
    <h1>📜 Legal Agreement Blockchain Node</h1>

    <form action="/add_agreement" method="post">
        <input type="text" name="party_a" placeholder="Party A Name" required>
        <input type="text" name="party_b" placeholder="Party B Name" required>
        <input type="text" name="agreement_title" placeholder="Agreement Title" required>
        <textarea name="terms" placeholder="Agreement Terms" rows="4" required></textarea>
        <input type="date" name="date_signed" required>
        <button type="submit">Submit Agreement</button>
    </form>

    <h2>🔗 Blockchain</h2>
    {% for block in chain %}
        <div class="block">
            <pre>{{ block | tojson(indent=2) }}</pre>
        </div>
    {% endfor %}
</body>
</html>
'''

# -------------------------
# Flask Routes
# -------------------------
@app.route('/')
def index():
    return render_template_string(template, chain=blockchain.chain)

@app.route('/add_agreement', methods=['POST'])
def add_agreement():
    data = request.form

    # Add new transaction
    blockchain.add_transaction(
        data['party_a'],
        data['party_b'],
        data['agreement_title'],
        data['terms'],
        data['date_signed']
    )

    # Auto mine block immediately after adding transaction
    last_proof = blockchain.last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    previous_hash = blockchain.hash(blockchain.last_block)
    blockchain.create_block(proof, previous_hash)

    return render_template_string(template, chain=blockchain.chain)

@app.route('/chain', methods=['GET'])
def full_chain():
    return jsonify({'chain': blockchain.chain, 'length': len(blockchain.chain)})

# -------------------------
# Run App
# -------------------------
if __name__ == '__main__':
    app.run(debug=True)
