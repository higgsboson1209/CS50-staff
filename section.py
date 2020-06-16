import csv
import random

capacity = 5
leaders = 4

def main():
	availabilities = 'example1.csv'
	with open(availabilities) as csvfile:
		readCSV = csv.reader(csvfile, delimiter=',')
		count = 0
		students = dict()
		for row in readCSV:
			if count != 0:
				# print(row[1:])
				# print(len(row[2].split(',')))
				students[row[1]] = row[2].split(',')
				students[row[1]] = [t.strip() for t in students[row[1]]]
			count += 1
		students = {k: v for k, v in sorted(students.items(), key=lambda item: len(item[1]))}
		print(students)
		times = dict()
		i = 0
		s_lst = list(students)
		while len(times) < leaders:
			slots = students[s_lst[i]]
			success = False
			while not success:
			# times[students[]]
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
		print(times)
		# TODO: add load balancing
		counter = 1
		total = 0
		times = {k: v for k, v in sorted(times.items(), key=lambda item: item[0])}
		for t in times:
			print(f"Section #{counter} ({t}): {sorted(times[t])}")
			counter += 1
			total += len(times[t])
		print(f"Score: {round(total / (count - 1) * 100, 2)}%")


# class Section():

if __name__ == "__main__":
	main()