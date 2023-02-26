#include<stdio.h>
#include<stdlib.h>

# define TESTS 4

typedef struct student_init_data student_init_data;
struct student_init_data {
	int id;
	int *grades;
	int grades_amount;
};

typedef struct student_processed_data student_processed_data;
struct student_processed_data {
	int id;
	int average;
};

typedef struct statistics statistics;
struct statistics {
	student_processed_data *below_average;
	int below_average_amount;
	student_processed_data *above_average;
	int above_average_amount;
	int average;
};

int student_amount;
student_init_data* student_init_array;

int* input_data(int grades_amount) {
	int i, *grades;

	grades = (int*)malloc(sizeof(int) * grades_amount);
	
	for (i = 0; i < grades_amount; i++) {
		printf("\tEnter grade number %d: ", i + 1);
		scanf_s("%d", &grades[i]);
	}

	return grades;
}

int student_average(int* grades) {
	int average = 0, i, grades_amount;

	grades_amount = TESTS;
	for (i = 0; i < grades_amount; i++) {
		average += grades[i];
	}

	average /= grades_amount;

	return average;
}

int total_average(int* averages) {
	int average = 0, i, averages_amount;

	averages_amount = student_amount;
	for (i = 0; i < averages_amount; i++) {
		average += averages[i];
	}

	average /= averages_amount;

	return average;
}

statistics* classification(student_init_data* student_init_array) {
	int i, average, *averages, below_average_amount = 0, above_average_amount = 0, current_below_average, current_above_average;
	student_processed_data* student_processed_array, *below_average, *above_average;
	statistics stats;

	student_processed_array = (student_processed_data*)malloc(sizeof(student_processed_data) * student_amount);
	averages = (int*)malloc(sizeof(int) * student_amount);

	for (i = 0; i < student_amount; i++) {
		printf("Student id %d\n", i);
		student_init_array[i].id = i;
		student_init_array[i].grades = input_data(TESTS);
		student_init_array[i].grades_amount = TESTS;

		student_processed_array[i].id = student_init_array[i].id;
		student_processed_array[i].average = student_average(student_init_array[i].grades);

		averages[i] = student_processed_array[i].average;
	}

	average = total_average(averages);

	for (i = 0; i < student_amount; i++) {
		if (student_processed_array[i].average < average) {
			below_average_amount++;
		}
		else {
			above_average_amount++;
		}
	}

	below_average = (student_processed_data*)malloc(sizeof(student_processed_data) * below_average_amount);
	above_average = (student_processed_data*)malloc(sizeof(student_processed_data) * above_average_amount);

	current_below_average = 0;
	current_above_average = 0;

	for (i = 0; i < student_amount; i++) {
		if (student_processed_array[i].average < average) {
			below_average[current_below_average] = student_processed_array[i];
			current_below_average++;
		}
		else {
			above_average[current_above_average] = student_processed_array[i];
			current_above_average++;
		}
	}

	stats.average = average;
	stats.below_average = below_average;
	stats.below_average_amount = below_average_amount;
	stats.above_average = above_average;
	stats.above_average_amount = above_average_amount;

	free(averages);
	free(student_processed_array);

	return &stats;
}

void print_tab(statistics stats) {
	int i;

	printf("\n\nAverage: %d\n", stats.average);
	
	printf("Below average:\n");
	for (i = 0; i < stats.below_average_amount; i++) {
		printf("\tStudent %d: %d\n", stats.below_average[i].id, stats.below_average[i].average);
	}
	printf("Total below average: %d\n\n", stats.below_average_amount);

	printf("Above average:\n");
	for (i = 0; i < stats.above_average_amount; i++) {
		printf("\tStudent %d: %d\n", stats.above_average[i].id, stats.above_average[i].average);
	}
	printf("Total above average: %d\n", stats.above_average_amount);
}

void free_memory(student_init_data* students_init_array, statistics stats) {
	int i;

	printf("%d\n", stats.average);

	for (i = 0; i < student_amount; i++) {
		free(students_init_array[i].grades);
	}
	free(students_init_array);

	printf("%d\n", stats.average);

	free(stats.below_average);
	free(stats.above_average);
}

int main(int argc, char* argv[]) {
	statistics *stats;

	printf("Enter amount of students: ");
	scanf_s("%d", &student_amount);

	student_init_array = (student_init_data*)malloc(sizeof(student_init_data) * student_amount);

	stats = classification(student_init_array);
	printf("%d\n", stats->average);
	printf("%d\n", stats->average);
	print_tab(*stats);
	printf("%d\n", stats->average);
	free_memory(student_init_array, *stats);

	return(0);
}
