import csv
import random

leaders = 4
limit = 50
offset = 0
availabilities = 'example1.csv'

def generate():
	global offset
	iteration = 0
	sofar = 0
	while sofar < 100:
		if iteration == limit:
			offset += 1
			iteration = 0
			if offset == 30:
				print(best_result)
				print(f"Score: {best_score}%")
				break
		with open(availabilities) as csvfile:
			readCSV = csv.reader(csvfile, delimiter=',')
			iteration += 1
			n_students = 0
			students = dict()
			for row in readCSV:
				if n_students != 0:
					# print(row[1:])
					# print(len(row[2].split(',')))
					students[row[1]] = row[2].split(',')
					students[row[1]] = [t.strip() for t in students[row[1]]]
				n_students += 1
			n_students -= 1
			capacity = offset
			if (n_students) % leaders == 0:
				capacity += (n_students) // leaders
			else:
				capacity += ((n_students) // leaders) + 1
			### https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value	
			students = {k: v for k, v in sorted(students.items(), key=lambda item: len(item[1]))}
			# print(students)
			times = dict()
			i = 0
			s_lst = list(students)
			while len(times) < leaders:
				slots = students[s_lst[i]]
				success = False
				while not success:
					sel = random.choice(slots)
					# sel = None
					best = capacity
					for t in random.sample(slots, len(slots)):
						if t in times:
							if len(times[t]) < best:
								sel = t
								best = len(times[t])
					assigned = times.get(sel, set())
					if len(assigned) < capacity:
						assigned.add(s_lst[i])
						times[sel] = assigned
						slots.remove(sel)
						success = True
						students.pop(s_lst[i], None)
						s_lst.pop(i)
				if not students:
					break
				i = (i + 1) % len(students)
			i = 0
			while len(s_lst) and i < len(s_lst):
				found = False
				for t in students[s_lst[i]]:
					if t in times and len(times[t]) < capacity:
						times[t].add(s_lst[i])
						s_lst.pop(i)
						found = True
						break
				if not found:
					i = (i + 1) % len(s_lst)
			# print(times)
			total = 0
			times = {k: v for k, v in sorted(times.items(), key=lambda item: item[0])}
			for t in times:				
				total += len(times[t])
			# TODO: account for load balancing in score
			score = round(total / (n_students) * 100, 2)
			if score > sofar:
				sofar = score
				best_result = ''
				sec_num = 1
				for t in times:
					best_result += f"Section #{sec_num} ({t}): {sorted(times[t])}"
					if sec_num != len(times):
						best_result += "\n"
						sec_num += 1
				best_score = score
				if sofar == 100:
					print(best_result)
					print(f"Score: {best_score}%")

if __name__ == "__main__":
	generate()
