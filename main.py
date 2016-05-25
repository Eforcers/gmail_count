#!/usr/bin/python
import os
import sys
import csv
import traceback
from constants import GMAIL_LABELS
from helper import GmailHelper


def main():
    file = os.path.join(os.getcwd(), sys.argv[1])
    with open(file, 'rt') as csvfile:
        rows = [row for row in csv.reader(csvfile)]
        column_names = [name.strip() for name in rows[0]]
        email_index = column_names.index('email')

        output_file = 'message-count-users-output.csv'

        with open(output_file, 'wb') as output_file:
            writer = csv.writer(output_file, delimiter=',', quotechar='|',
                                quoting=csv.QUOTE_NONE)
            headers = ['email',
                       'source_message_count',
                       ]
            writer.writerow(headers)

            for row in rows[1:]:
                email = ''
                count = 0
                count_pages = 0
                try:
                    email = row[email_index].strip()
                    # Connect to the source to the all message folder
                    gmail_helper = GmailHelper(user_email=email)
                    page_token = None
                    while True:
                        count_pages += 1

                        messages, page_token = gmail_helper.list_messages(
                            q="", page_token=page_token)
                        count += len(messages)
                        if not page_token:
                            break
                    print count_pages

                    new_row = []
                    new_row.append(str(email))
                    new_row.append(str(count))
                    writer.writerow(new_row)
                except Exception as e:
                    print 'Error while connecting to get message count for ' \
                          'account[%s]: %s -> %s' % (email, e,
                                                     traceback.format_exc())


if __name__ == "__main__":
    main()