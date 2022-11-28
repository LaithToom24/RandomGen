import java.lang.Math;
import java.util.Scanner;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

class Experiment1{
  public static void main(String[] args){
    Scanner scan = new Scanner(System.in);

    System.out.print("Please enter a word: ");
    String userString = scan.nextLine();
    
    String fileName = "resultsFor_"+userString+".txt";
    try {
      File dataFile = new File(fileName);
      dataFile.createNewFile();
    } catch (IOException e){
      System.out.print(e+" has unfortunately occured\n");
    }
    
    randomizedGenerationMethod1(userString);
    randomizedGenerationMethod2(userString);
    
  }

  public static void randomizedGenerationMethod1(String str){
    String generatedStr = "";
    int wordCount = 0;

    boolean run = true;
    while (run){
      for (int i = 0; i < str.length(); i++){
        generatedStr += "aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ ".charAt((int)(Math.random()*53)) + "";
      }

      wordCount++;
      if (generatedStr.equals(str) != true && wordCount < 10000000)
        generatedStr = "";
      else
        run = false;
    }

    if (generatedStr.equals(str))
      System.out.print("\""+generatedStr+"\" was generated in "+wordCount+" words :)\n");
    else
      System.out.print("It's been "+wordCount+" words and we still haven't generated your word! All we have is "+generatedStr+". ;-;\n");
    
    try{
      FileWriter writer = new FileWriter("output.txt", true);
      writer.write(0+","+wordCount);
      writer.close();
    } catch (IOException e){
      System.out.print(e+" has unfortunately occured\n");
    }
  }

  public static void randomizedGenerationMethod2(String str){
    String generatedStr = "";
    char generatedLetter;
    int letterCount = 0;

    boolean run = true;
    while (run){
      for (int i = 0; i < str.length();){
        generatedLetter = "aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ ".charAt((int)(Math.random()*53));
        letterCount++;
        if (generatedLetter == str.charAt(i)){
          /*
          System.out.println("\n"+letterCount);
          letterCount = 0
          */
          generatedStr += generatedLetter+"";
          i++;
        }
      }
      run = false;
    }

    System.out.print("\""+generatedStr+"\" was generated in "+letterCount+" letters, which is roughly equivalent to "+letterCount/generatedStr.length()+" words. :)\n");
    
    try{
      FileWriter writer = new FileWriter("output.txt", true);
      writer.write(0+","+letterCount);
      writer.close();
    } catch (IOException e){
      System.out.print(e+" has unfortunately occured\n");
    }
  }
}
