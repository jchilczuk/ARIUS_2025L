package com.example.zad6_metmuseumapi;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.ListView;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;

// Main activity of the application – responsible for displaying a list of artworks
public class MainActivity extends Activity {
    ListView listView;
    TextView resultsTextView;
    ProgressBar progressBar;
    ArrayList<Artwork> artworks = new ArrayList<>();
    private static final String TAG = "MainActivity";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Bind UI components
        listView = findViewById(R.id.artList);
        resultsTextView = findViewById(R.id.resultsTextView);
        progressBar = findViewById(R.id.progressBar);

        Log.d(TAG, "onCreate: Starting AsyncTask to load artworks");
        new LoadArtworks().execute(); // Start async loading of artworks from the API

        // Handle item clicks in the list to open a detail view
        listView.setOnItemClickListener((parent, view, position, id) -> {
            Artwork selected = artworks.get(position);
            Log.d(TAG, "Item clicked: " + selected.title);

            // Pass selected artwork data to detail activity
            Intent intent = new Intent(MainActivity.this, ArtDetailsActivity.class);
            intent.putExtra("title", selected.title);
            intent.putExtra("image", selected.imageUrl);
            intent.putExtra("artist", selected.artist);
            intent.putExtra("medium", selected.medium);
            intent.putExtra("dimensions", selected.dimensions);
            intent.putExtra("objectDate", selected.objectDate);
            startActivityForResult(intent, 100); // Start DetailActivity expecting result
        });
    }

    // AsyncTask to fetch artwork data from the MET API in the background
    @SuppressLint("StaticFieldLeak")
    class LoadArtworks extends AsyncTask<Void, Void, Void> {

        // Before the background task begins – show progress
        @SuppressLint("SetTextI18n")
        @Override
        protected void onPreExecute() {
            super.onPreExecute();
            Log.d(TAG, "onPreExecute: Showing progress bar");
            progressBar.setVisibility(View.VISIBLE);
            resultsTextView.setText("Loading artworks...");
        }

        // Main background task: fetch objectIDs and then fetch each artwork
        @Override
        protected Void doInBackground(Void... voids) {
            try {
                // Step 1: Perform search query to get objectIDs
                URL url = new URL("https://collectionapi.metmuseum.org/public/collection/v1/search?hasImages=true&q=Vincent van Gogh");
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream()));
                StringBuilder result = new StringBuilder();
                String line;

                while ((line = reader.readLine()) != null) {
                    result.append(line);
                }

                JSONObject searchResult = new JSONObject(result.toString());
                JSONArray ids = searchResult.getJSONArray("objectIDs");

                // Step 2: Fetch detailed data for each object, up to 30 valid ones
                int validCount = 0;
                for (int i = 0; i < ids.length(); i++) {
                    if (validCount >= 20) break; // Stop after 30 valid artworks

                    int objectId = ids.getInt(i);
                    Log.d(TAG, "Fetching object ID: " + objectId);

                    try {
                        URL objectUrl = new URL("https://collectionapi.metmuseum.org/public/collection/v1/objects/" + objectId);
                        HttpURLConnection objectConn = (HttpURLConnection) objectUrl.openConnection();
                        BufferedReader objectReader = new BufferedReader(new InputStreamReader(objectConn.getInputStream()));
                        StringBuilder objectResult = new StringBuilder();

                        while ((line = objectReader.readLine()) != null) {
                            objectResult.append(line);
                        }

                        // Parse artwork metadata
                        JSONObject obj = new JSONObject(objectResult.toString());
                        String image = obj.optString("primaryImageSmall");
                        String title = obj.optString("title");
                        String artist = obj.optString("artistDisplayName");
                        String medium = obj.optString("medium");
                        String dimensions = obj.optString("dimensions");
                        String objectDate = obj.optString("objectDate");

                        // Only add artworks that have both an image and a title
                        if (!image.isEmpty() && !title.isEmpty()) {
                            artworks.add(new Artwork(title, image, artist, medium, dimensions, objectDate));
                            validCount++;
                            Log.d(TAG, "Added: " + title);
                        } else {
                            Log.d(TAG, "Skipped object (no image/title): " + objectId);
                        }

                    } catch (Exception ex) {
                        Log.w(TAG, "Skipping invalid objectID " + objectId + ": " + ex.toString());
                    }
                }

            } catch (Exception e) {
                Log.e(TAG, "Error fetching artworks", e);
            }

            return null;
        }

        // After background task: hide progress and update UI
        @SuppressLint("SetTextI18n")
        @Override
        protected void onPostExecute(Void aVoid) {
            Log.d(TAG, "onPostExecute: Finished loading, updating UI");
            progressBar.setVisibility(View.GONE);
            resultsTextView.setText("Loaded " + artworks.size() + " artworks");
            ArtworkAdapter adapter = new ArtworkAdapter(MainActivity.this, artworks);
            listView.setAdapter(adapter); // Bind data to the ListView
        }
    }

    // Handle return from DetailActivity
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == 100 && resultCode == RESULT_OK) {
            String message = data.getStringExtra("message");
            Toast.makeText(this, message, Toast.LENGTH_SHORT).show();
            Log.d(TAG, "onActivityResult: Received message - " + message);
        }
    }
}
