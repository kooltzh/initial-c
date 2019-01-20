from uuid import uuid4
import pickle
from native_blockchain import *


from flask import Flask, jsonify, request, render_template

# Instantiate the Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    # only mine the block if have transactions
    if len(blockchain.current_transactions) == 0:
        response = {
            'message': "No block mined since have no new transaction",
            'index': last_block['index'],
            'transactions': last_block['transactions'],
            'proof': last_block['proof'],
            'previous_hash': last_block['previous_hash'],
        }
        return jsonify(response), 201
    else:
        # Forge the new Block by adding it to the chain
        previous_hash = blockchain.hash(last_block)
        block = blockchain.new_block(previous_hash)

        response = {
            'message': "New Block Forged",
            'index': block['index'],
            'transactions': block['transactions'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash'],
        }
        return jsonify(response), 200


@app.route('/save', methods=['GET'])
def save_blockchain():
    name = request.args.get('name', 'blockchain.bin')

    with open(name, 'wb') as fp:
        pickle.dump(blockchain, fp)
    response = {
        'message': f'saved as {name}'
    }

    return jsonify(response), 200


@app.route('/load', methods=['GET'])
def load_blockchain():
    name = request.args.get('name', 'blockchain.bin')

    with open(name, 'rb') as fp:
        blockchain = pickle.load(fp)

    response = {
        'message': f'loaded as {name}'
    }

    if blockchain.valid_chain(blockchain.chain):
        return jsonify(response), 200
    else:
        return 'Loaded not successful, 401'


@app.route('/msg/new', methods=['POST'])
def new_message():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'original_msg', 'modified_msg', 'similarity']
    if values is None:
        return 'Values is None', 400
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.new_message(values['sender'], values['recipient'], values['original_msg'],
                                   values['modified_msg'], values['similarity'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200


@app.route('/msg/trace', methods=['POST', 'GET'])
def trace_source():
    values = request.get_json()
    if not values:
        values = request.args
    # Check that the required fields are in the POST'ed data
    required = ['msg']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # query the blockchain to find the source
    search_str = values['msg']
    list_user_msg = []

    avail_chains = blockchain.chain
    first = True
    for chain in reversed(avail_chains):
        trans = chain['transactions']
        for tran in reversed(trans):
            if tran['modified_msg'] == search_str:
                if first:
                    first = False
                    user_msg = {
                        'user': tran['recipient'],
                        'msg': tran['modified_msg']
                    }
                    list_user_msg.append(user_msg)
                user_msg = {
                    'user': tran['sender'],
                    'msg': tran['original_msg']
                }
                list_user_msg.append(user_msg)
                search_str = tran['original_msg']

    return render_template('trace.html', items = list_user_msg)


@app.route('/', methods=['GET'])
def main_page():
    return 'Hello world from flask_blockchain. Jiayous :D'


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    # app.run(host='0.0.0.0', port=port)
    app.run(port=5020, debug=True)
