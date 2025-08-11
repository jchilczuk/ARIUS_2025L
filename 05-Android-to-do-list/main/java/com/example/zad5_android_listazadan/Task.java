package com.example.zad5_android_listazadan;

import android.annotation.SuppressLint;
import java.io.Serializable;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

// Task class represents a single task in the task list
// It implements Serializable so it can be passed between activities via Intent
public class Task implements Serializable {

    // Enum representing the possible status values of a task
    public enum Status { NOT_DONE, DONE, OVERDUE }

    // Fields representing the task's data
    private final String title;        // Title of the task
    private final String description;  // Description/details of the task
    private final String deadline;     // Deadline in the format "yyyy-MM-dd HH:mm"
    private Status status;             // Current status of the task

    // Constructor to initialize all task fields
    public Task(String title, String description, String deadline, Status status) {
        this.title = title;
        this.description = description;
        this.deadline = deadline;
        this.status = status;
    }

    // Getters to retrieve task information
    public String getTitle() { return title; }
    public String getDescription() { return description; }
    public String getDeadline() { return deadline; }
    public Status getStatus() { return status; }

    // Setter to change the task status
    public void setStatus(Status status) { this.status = status; }

    // isOverdue method determines whether the task is overdue
    public boolean isOverdue() {
        // If task is already marked as DONE or OVERDUE, no need to check again
        if (status == Status.DONE || status == Status.OVERDUE) return false;

        try {
            // Parse the deadline using date and time format
            @SuppressLint("SimpleDateFormat")
            SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm");
            // Convert the deadline string to a Date object
            Date deadlineDate = sdf.parse(deadline);
            // Get the current date and time
            Date now = new Date();
            // Return true if current date and time is after the deadline
            return now.after(deadlineDate);
        } catch (ParseException e) {
            // If parsing fails, assume the task is not overdue
            e.printStackTrace();
            return false;
        }
    }

}
