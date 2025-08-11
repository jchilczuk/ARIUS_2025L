package com.example.zad6_metmuseumapi;
public class Artwork {
    public String title;
    public String imageUrl;
    public String artist;
    public String medium;
    public String dimensions;
    public String objectDate;

    //Model class for artwork data
    public Artwork(String title, String imageUrl, String artist, String medium, String dimensions, String objectDate) {
        this.title = title;
        this.imageUrl = imageUrl;
        this.artist = artist;
        this.medium = medium;
        this.dimensions = dimensions;
        this.objectDate = objectDate;
    }
}
