from flask import Flask, render_template, request, jsonify, redirect, url_for
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  

allocation_results = []  
csv_content = ""  

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results')
def results():
    return render_template('results.html', allocation=allocation_results, csv_content=csv_content)

@app.route('/allocate', methods=['POST'])
def allocate():
    global allocation_results, csv_content
    try:
        group_info_file = request.files['groupInfoFile']
        hostel_info_file = request.files['hostelInfoFile']

        group_info_df = pd.read_csv(group_info_file)
        hostel_info_df = pd.read_csv(hostel_info_file)

        allocation_results, csv_content = allocate_rooms(group_info_df, hostel_info_df)

        return jsonify({"status": "success"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def allocate_rooms(group_info_df, hostel_info_df):
    allocation = []
    hostels = hostel_info_df.to_dict('records')
    csv_content = []

    for hostel in hostels:
        hostel['Occupancy'] = 0

    for _, group in group_info_df.iterrows():
        group_id = group['GroupID']
        members = group['Members']
        gender = group['Gender']
        allocated = False

        for hostel in hostels:
            if (gender == 'Boys' and hostel['Gender'] == 'Boys' and 
                hostel['Occupancy'] + members <= hostel['Capacity']):
                allocation.append({
                    "GroupID": group_id,
                    "HostelName": hostel['HostelName'],
                    "RoomNumber": hostel['RoomNumber'],
                    "MembersAllocated": members
                })
                hostel['Occupancy'] += members
                csv_content.append(f"{group_id},{hostel['HostelName']},{hostel['RoomNumber']},{members}\n")
                allocated = True
                break
            elif (gender == 'Girls' and hostel['Gender'] == 'Girls' and 
                  hostel['Occupancy'] + members <= hostel['Capacity']):
                allocation.append({
                    "GroupID": group_id,
                    "HostelName": hostel['HostelName'],
                    "RoomNumber": hostel['RoomNumber'],
                    "MembersAllocated": members
                })
                hostel['Occupancy'] += members
                csv_content.append(f"{group_id},{hostel['HostelName']},{hostel['RoomNumber']},{members}\n")
                allocated = True
                break

        if not allocated:
            allocation.append({
                "GroupID": group_id,
                "HostelName": "Not Allocated",
                "RoomNumber": "N/A",
                "MembersAllocated": members
            })
            csv_content.append(f"{group_id},Not Allocated,N/A,{members}\n")

    return allocation, ''.join(csv_content)

if __name__ == '__main__':
    app.run(debug=True)
