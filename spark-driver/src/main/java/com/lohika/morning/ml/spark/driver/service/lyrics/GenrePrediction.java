package com.lohika.morning.ml.spark.driver.service.lyrics;

public class GenrePrediction {

    private String genre;
    private Double popProbability;
    private Double countryProbability;
    private Double bluesProbability;
    private Double jazzProbability;
    private Double reggaeProbability;
    private Double rockProbability;
    private Double hipHopProbability;
    private Double electroProbability;

    // Constructor matching the CommonLyricsPipeline call
    public GenrePrediction(String genre,
                           Double popProbability,
                           Double countryProbability,
                           Double bluesProbability,
                           Double jazzProbability,
                           Double reggaeProbability,
                           Double rockProbability,
                           Double hipHopProbability,
                           Double electroProbability) {
        this.genre = genre;
        this.popProbability = popProbability;
        this.countryProbability = countryProbability;
        this.bluesProbability = bluesProbability;
        this.jazzProbability = jazzProbability;
        this.reggaeProbability = reggaeProbability;
        this.rockProbability = rockProbability;
        this.hipHopProbability = hipHopProbability;
        this.electroProbability = electroProbability;
    }

    // Optional: single-arg constructor for fallback case
    public GenrePrediction(String genre) {
        this.genre = genre;
    }

    // Getters and setters
    public String getGenre() {
        return genre;
    }

    public void setGenre(String genre) {
        this.genre = genre;
    }

    public Double getPopProbability() {
        return popProbability;
    }

    public Double getCountryProbability() {
        return countryProbability;
    }

    public Double getBluesProbability() {
        return bluesProbability;
    }

    public Double getJazzProbability() {
        return jazzProbability;
    }

    public Double getReggaeProbability() {
        return reggaeProbability;
    }

    public Double getRockProbability() {
        return rockProbability;
    }

    public Double getHipHopProbability() {
        return hipHopProbability;
    }

    public Double getElectroProbability() {
        return electroProbability;
    }
}
