from functools import reduce


class TransactionService:
    def crombobulate(self, entry):
        if len(entry['transactions']) == 0:
            return None

        paid_total = reduce(lambda x, y: x + y, [t['paid'] for t in entry['transactions']])
        owes_total = reduce(lambda x, y: x + y, [t['owes'] for t in entry['transactions']])

        # TODO it's possible that entry['total'] is not an int...
        if paid_total != owes_total or owes_total != entry['total']:
            # TODO should this be an exception?
            return None

        overpaid = []
        underpaid = []

        # TODO we're doing nothing with label here -- probably should

        for transaction in entry['transactions']:
            node = {
                'user_id': transaction['payer'],
                'zerosum': transaction['paid'] - transaction['owes']
            }

            if node['zerosum'] < 0:
                underpaid.append(node)
            if node['zerosum'] > 0:
                overpaid.append(node)

        q = []
        log = []

        while len(overpaid) > 0:
            overpaid = sorted(overpaid, key=lambda t: t['zerosum'])
            underpaid = sorted(underpaid, key=lambda t: t['zerosum'], reverse=True)

            give_to = overpaid.pop()
            take_from = underpaid.pop()

            log.append(str(give_to['zerosum']) + " vs " + str(take_from['zerosum']))

            if give_to['zerosum'] + take_from['zerosum'] >= 0:
                log.append("in if")
                give_to['zerosum'] += take_from['zerosum']
                owed = abs(take_from['zerosum'])
                take_from['zerosum'] = 0
            else:
                log.append("in else")
                take_from['zerosum'] += give_to['zerosum']
                owed = give_to['zerosum']
                give_to['zerosum'] = 0

            q.append(str(take_from['user_id']) + ' owes ' + str(give_to['user_id']) + " $" + str(owed))

            if give_to['zerosum'] != 0:
                overpaid.append(give_to)

            if take_from['zerosum'] != 0:
                underpaid.append(take_from)

        return {"q": q, "log": log}
