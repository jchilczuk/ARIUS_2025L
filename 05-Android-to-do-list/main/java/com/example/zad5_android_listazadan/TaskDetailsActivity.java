package com.example.zad5_android_listazadan;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.widget.*;

//Class TaskDetailsActivity displays details of a single task
public class TaskDetailsActivity extends Activity {

    // Task object passed from MainActivity
    Task task;

    // Index of the task in the original list
    int index;

    // Buttons to mark task as done or not done
    Button btnDone, btnNotDone;

    @SuppressLint("SetTextI18n")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_task_details);

        // Link UI components to their views
        TextView titleText = findViewById(R.id.titleText);
        TextView descriptionText = findViewById(R.id.descriptionText);
        TextView deadlineText = findViewById(R.id.deadlineText);
        TextView statusText = findViewById(R.id.statusText); // Text view to display task status

        btnDone = findViewById(R.id.btnDone);
        btnDone.setBackgroundColor(getResources().getColor(R.color.light_green, null)); // Set light green background

        btnNotDone = findViewById(R.id.btnNotDone);
        btnNotDone.setBackgroundColor(getResources().getColor(R.color.light_red, null)); // Set light red background

        // Retrieve task and index from Intent
        Intent intent = getIntent();
        task = (Task) intent.getSerializableExtra("task");
        index = intent.getIntExtra("index", -1);

        // Display task data in the views
        titleText.setText(task.getTitle());
        descriptionText.setText("Details: " + task.getDescription());
        deadlineText.setText("Deadline: " + task.getDeadline());

        // Check if the task is overdue and update status accordingly
        if (task.isOverdue()) {
            task.setStatus(Task.Status.OVERDUE);
        }

        // Update button states and display status text
        updateButtonStates();
        updateStatusText(statusText);

        // Mark task as done when "Done" button is clicked
        btnDone.setOnClickListener(v -> {
            task.setStatus(Task.Status.DONE);
            updateButtonStates();
            updateStatusText(statusText);
            returnResult();
        });

        // Mark task as not done when "Not Done" button is clicked
        btnNotDone.setOnClickListener(v -> {
            task.setStatus(Task.Status.NOT_DONE);
            updateButtonStates();
            updateStatusText(statusText);
            returnResult();
        });
    }

    // Disable buttons if task is overdue
    private void updateButtonStates() {
        boolean enabled = task.getStatus() != Task.Status.OVERDUE;
        btnDone.setEnabled(enabled);
        btnNotDone.setEnabled(enabled);
    }

    // Update the status display text and color
    @SuppressLint("SetTextI18n")
    private void updateStatusText(TextView statusText) {
        String statusString;
        int color;

        switch (task.getStatus()) {
            case DONE:
                statusString = "WYKONANE";
                color = getResources().getColor(R.color.green, null);
                break;
            case NOT_DONE:
                statusString = "NIEWYKONANE";
                color = getResources().getColor(R.color.red, null);
                break;
            case OVERDUE:
            default:
                statusString = "PRZETERMINOWANE";
                color = getResources().getColor(R.color.orange, null);
                break;
        }

        statusText.setText("Status: " + statusString);
        statusText.setTextColor(color);
    }

    // Return updated task and its index to the MainActivity
    private void returnResult() {
        Intent result = new Intent();
        result.putExtra("task", task);
        result.putExtra("index", index);
        setResult(RESULT_OK, result);
        finish(); // Close the details activity
    }
}
