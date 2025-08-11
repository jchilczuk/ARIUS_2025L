package com.example.zad5_android_listazadan;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.widget.ListView;
import java.util.ArrayList;

// Class MainActivity displays a list of tasks
public class MainActivity extends Activity {
    // List to store all task objects
    ArrayList<Task> tasks;

    // Adapter that connects the data with the ListView
    TaskAdapter adapter;

    // Request code to identify the result from the detail activity
    final int REQUEST_CODE = 1;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // Set the layout for this activity
        setContentView(R.layout.activity_main);

        // Find ListView defined in the layout
        ListView listView = findViewById(R.id.taskListView);

        // Load task data from resources (string-arrays)
        String[] titles = getResources().getStringArray(R.array.task_titles);
        String[] descriptions = getResources().getStringArray(R.array.task_descriptions);
        String[] deadlines = getResources().getStringArray(R.array.task_deadlines);

        // Initialize the task list using the loaded resource arrays
        tasks = new ArrayList<>();
        for (int i = 0; i < titles.length; i++) {
            tasks.add(new Task(titles[i], descriptions[i], deadlines[i], Task.Status.NOT_DONE));
        }

        // Initialize the adapter and connect it to the ListView
        adapter = new TaskAdapter(this, tasks);
        listView.setAdapter(adapter);

        // Handle click on a task item to show its details in a new activity
        listView.setOnItemClickListener((parent, view, position, id) -> {
            Intent intent = new Intent(MainActivity.this, TaskDetailsActivity.class);
            intent.putExtra("task", tasks.get(position));
            intent.putExtra("index", position);
            startActivityForResult(intent, REQUEST_CODE);
        });
    }

    // Handle the result returned from TaskDetailsActivity
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        // If the result is from the expected activity and it was successful
        if (requestCode == REQUEST_CODE && resultCode == RESULT_OK) {
            Task updated = (Task) data.getSerializableExtra("task");
            int index = data.getIntExtra("index", -1);

            // Check if the task is overdue and update its status accordingly
            if (updated.isOverdue()) {
                updated.setStatus(Task.Status.OVERDUE);
            }

            // Update the task in the list and refresh the UI
            if (index >= 0) {
                tasks.set(index, updated);
                adapter.notifyDataSetChanged();
            }
        }
    }
}
