import pandas as pd


with open("bigquery_full.csv") as fh:
	df = pd.read_csv(fh)

counts = df["gh_project_name"].value_counts()
counts = counts[counts > 50]
counts = counts[counts < 200]
projects = list(counts.keys())

for project in projects:
	filtered_df = df[df["gh_project_name"] == project]
	status_counts = filtered_df["tr_status"].value_counts()
	if not all(count > 5 for count in status_counts):
		continue
	with open("new-text-files/" + project.replace("/", "|") + ".txt", "w") as fh:
		filtered_df.to_csv(fh, index=False, header=False)
