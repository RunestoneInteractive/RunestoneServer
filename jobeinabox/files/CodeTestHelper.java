import java.io.*;
import java.lang.reflect.*;

import java.util.Arrays;

import java.util.regex.Pattern;
import java.util.regex.Matcher;

import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.charset.StandardCharsets;

import static org.junit.Assert.*;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

/**
 * The test class CodeTestHelper provides methods for testing different types of ActiveCode Assignments. 
 * This class provides helper methods to make writing test classes easier. Methods should be tested even if they
 * do not exist.
 *
 * @author  Kate McDonnell
 * @version 0.3.5
 * @since 2020-07-28
 * 
 * 
 */
public class CodeTestHelper
{
    public static boolean replit = false;
    public static boolean sort = false;

    private static String results = "";
    private static String mainOutput = "";
    private String errorMessage = "";

    private Class<?> c;
    private String className;

    private final double DEFAULT_ERROR = 0.005;

/* Constructors -----------------------------------------------------------------*/

    public CodeTestHelper() {
        String name = findMainMethod();
        setupClass(name);
    }
    
    public CodeTestHelper(String name) {
        setupClass(name);
    }

    public CodeTestHelper(String name, String input){
        inContent = new ByteArrayInputStream(input.getBytes(StandardCharsets.UTF_8));
        System.setIn(inContent);
        
        setupClass(name);
        
        System.setIn(System.in);

    }

    private void setupClass(String name) {
        try {
            this.className = name;
            this.c = Class.forName(this.className);

            mainOutput = getMethodOutput("main");

        } catch (Exception e1) {
            try {
                name = findMainMethod();

                if (!name.equals("main not found")){

                    this.className = name;
                    this.c = Class.forName(this.className);

                    mainOutput = getMethodOutput("main");
                }
                else {
                    System.out.println("No suitable main method found");
                }
            } catch (Exception e2) {
                System.out.println("No suitable main method found");
            }
        }
            
    }

    public void changeClass(String name) {
        try {
            this.className = name;
            this.c = Class.forName(this.className);

        } catch (Exception e1) {
            System.out.println("Class not found");
        }
    }



/* Output and Formatting Methods -----------------------------------------*/

    /**
     * This method will reset the final results variable so that multiple test runs will not continue to
     * add together.
     */
    public static void resetFinalResults() {
        results = "";
    }

    /**
     * This method will return the final results of all tests so that they can be printed to the screen.
     * It then resets the final results so that the list does not continually grow between different tests.
     * 
     * @return String list of final results in proper format
     */
    public static String getFinalResults() {
        String finalResults = "";//"Starting Output\n";
        finalResults += mainOutput; 
        //finalResults += "\nEnding Output";
        //finalResults += "\n--------------------------------------------------------";
        finalResults += "\nStarting Tests\n";

        if (sort) sortResults();

        finalResults += results.trim();
        finalResults += "\nEnding Tests";
        resetFinalResults();
        return finalResults;
    }

    /**
     * This method generates the proper results for the test and then performs the test by comparing the expected
     * and actual strings. Non-string variables should be made Strings before calling this method, using "" + num.
     * 
     * @param expected This is the String with the output we expect to get from the test
     * @param actual This is the String with the actual output from the test
     * @param msg This is the message that goes along with the test
     * @return boolean true if the test passed, false if it did not
     */
    public boolean getResults(String expected, String actual, String msg)
    {
        return getResults(false, false, expected, actual, msg);
    }

    public boolean getResultsRegex(String expected, String actual, String msg) {
        return getResults(true, false, expected, actual, msg);
    }

    public boolean getResultsRegEx(String expected, String actual, String msg) {
        return getResults(true, false, expected, actual, msg);
    }

    public boolean getResultsContains(String expected, String actual, String msg) {
        return getResults(false, true, expected, actual, msg);
    }
        
    public boolean getResults(boolean useRegex, boolean contain, String expected, String actual, String msg)
    {
        while (actual.contains("&ltimg") || actual.contains("<img")){
            int start = actual.contains("&ltimg") ? actual.indexOf("&ltimg") : actual.indexOf("<img");
            int end = actual.contains("&gt") ? actual.indexOf("&gt", start) : actual.indexOf(">", start);

            actual = actual.substring(0, start) + actual.substring(end+1);
            actual = actual.trim();

            //System.out.println(actual);
        }

        expected = expected.trim();
        actual = actual.trim();
        
        boolean passed = false;

        if (!passed && !contain) {
            String clnExp = cleanString(expected);
            String clnAct = cleanString(actual);

            passed = clnExp.equals(clnAct);
        }

        if (!passed && !expected.equals(""))
            contain = true;
        
        if (!passed && (useRegex || isRegex(expected)))
            passed = isMatch(actual, expected);

        if (!passed && contain && (useRegex || isRegex(expected)))
            passed = containsMatch(actual, expected);

        if (!passed && contain) {
            String clnExp = cleanString(expected);
            String clnAct = cleanString(actual);

            passed = clnAct.contains(clnExp);
        }

        String output = formatOutput(expected, actual, msg, passed);
        results += output + "\n";
        //System.out.println(output);

        return passed;
    }

    /**
     * This method assumes that you know whether the test passes or fails,
     * allowing you to have expected and actual be different. This is helpful
     * for testing a condtion where expected and actual might not be the same.
     * 
     * @param expected This is the String with the output we expect to get from the test
     * @param actual This is the String with the actual output from the test
     * @param msg This is the message that goes along with the test
     * @return boolean true if the test passed, false if it did not
     */
    public boolean getResults(String expected, String actual, String msg, boolean pass)
    {
        String output = formatOutput(expected, actual, msg, pass);
        results += output + "\n";
        //System.out.println(output);

        return pass;
    }

    /**
     * This method generates the proper results for the test and then performs the test by comparing the expected
     * and actual double values, within a margin of error of 0.005, so |expected - actual| < 0.005
     * 
     * @param expected This is the double with the output we expect to get from the test
     * @param actual This is the double with the actual output from the test
     * @param msg This is the message that goes along with the test
     * @return boolean true if the test passed, false if it did not, using 0.005 as the default error (delta)
     */
    public boolean getResults(double expected, double actual, String msg)
    {
        return getResults(expected, actual, 0.005, msg);
    }

    /**
     * This method generates the proper results for the test and then performs the test by comparing the expected
     * and actual double values, within a given margin of error.
     * 
     * @param expected This is the double with the output we expect to get from the test
     * @param actual This is the double with the actual output from the test
     * @param error This is the double error value (delta), so |expected - actual| < error
     * @param msg This is the message that goes along with the test
     * @return boolean true if the test passed, false if it did not, using given delta (error)
     */
    public boolean getResults(double expected, double actual, double error, String msg)
    {
        boolean passed = Math.abs(actual - expected) < error;

        String output = formatOutput(String.format("%.5f",expected), String.format("%.5f",actual), msg, passed);
        results += output + "\n";
        //System.out.println(output);

        return passed;
    }

    private String formatOutput(String expected, String actual, String msg, boolean passed) 
    {
        String output = "";

        expected = expected.trim();
        actual = actual.trim();
        msg = msg.trim();
        
        if (replit) {
            //expected = expected.replaceAll("\\n", " ").replaceAll("\\r", " ");
            //actual   = actual.replaceAll("\\n", " ").replaceAll("\\r", " ");
            output = "Expected: " + expected + "\nActual: " + actual + "\nMessage: " + msg + "\nPassed: " + passed + "\n";

        } else {
            expected = expected.replaceAll("\\n", "<br>").replaceAll("\\r", "<br>");
            actual   = actual.replaceAll("\\n", "<br>").replaceAll("\\r", "<br>");
            msg   = msg.replaceAll("\\n", "<br>").replaceAll("\\r", "<br>");
            output = "Expected: " + expected + "\tActual: " + actual + "\tMessage: " + msg + "\tPassed: " + passed;
        }
        
        return output;

        //return "Expected: " + expected + " Actual: " + actual + " Message: " + msg + " Passed: " + passed;
    }

/* Get Method output code --------------------------------------------------------*/
    /**
     * This method attempts to run a given method in a given class and returns the output if it succeeds
     *        - only works for methods with String[] args parameter at the moment ????
     * @param String name of the class where the method is written
     * @param String name of the method
     * @return String output of method - whatever has been printed to the console or returned
     */
    public String getMethodOutput(String methodName)// throws IOException
    {
        if (methodName.equals("main")) {
            return cleanQuotes(getMethodOutput(methodName, new String[1]));
        }
        return cleanQuotes(getMethodOutput(methodName, null));
    }

    /**
     * This method attempts to run a given method in a given class with the specified arguments and returns the output if it succeeds
     *        - only works for methods with String[] args parameter at the moment ????
     *        - is designed to return the output when any method has been called 
     * @param String name of the class where the method is written
     * @param String name of the method
     * @return String output of method - whatever has been printed to the console or returned
     */
    public String getMethodOutput(String methodName, Object[] args) {
        //System.out.println("Testing Method " + methodName + "... ");
        errorMessage = "";
        this.className = className;

        try {
            methods = c.getDeclaredMethods();

            for(Method m: methods) {
                if(m.getName().equals(methodName)) {                    
                    if(checkStaticMethod(m) && checkReturnType(m, "void")) {
                        return getStaticMethodOutput(m, args);
                    } else if (checkStaticMethod(m)) {
                        return getStaticMethodReturn(m, args);
                    } else {
                        return getInstanceMethodOutput(methodName, args);                            
                    }
                }

            } 

            if (errorMessage.equals(""))
                errorMessage = "Method " + methodName + " does not exist (2)";

        } catch (Exception e) {
            if (errorMessage.equals(""))
                errorMessage = "Class doesn't exist (2)";
        }

        return errorMessage;
    }

/* Class Testing Methods ---------------------------------------------------------*/

    private Object o;
    Method[] methods;

    private Object[] defaultTestValues;

    private String getInstanceMethodOutput(String methodName)// throws IOException
    {
        return getInstanceMethodOutput(methodName, null);
    }

    private String getInstanceMethodOutput(String methodName, Object[] args)// throws IOException
    {
        //System.out.println("Testing Method " + methodName + "... ");
        errorMessage = "";

        try {
            methods = c.getDeclaredMethods();

            for(Method m: methods) {
                if(m.getName().equals(methodName)) {

                    if(!checkStaticMethod(m) && checkReturnType(m, "void")) {
                        return getInstanceMethodOutput(m, null);
                    } else if (!checkStaticMethod(m)) {
                        Object o = getTestInstance();

                        if (o == null) {
                            return "Object could not be created (4)";
                        }

                        Object result = m.invoke(o, args);
                        return cleanResult(result);
                    } else {
                        errorMessage = "Method not static or not void (4)";                            
                    }
                }

            } 

            if (errorMessage.equals(""))
                errorMessage = "Method does not exist (4)";

        } catch (Exception e) {
            if (errorMessage.equals(""))
                errorMessage = "Class doesn't exist (4)";
        }

        return errorMessage;
    }

    private String cleanResult(Object result) {
        //System.out.println(result.getClass().getComponentType().isArray());

        if (result.getClass().isArray() ){
            if (result.getClass().getComponentType().isArray()) {
                String output = "[";
                Object[][] array = (Object[][]) result;
                for (int i = 0; i < array.length; i++) {
                    output += cleanResult(array[i]);
                    if (i != array.length - 1)
                        output += "\n";
                }
                return output + "]";
            } else if (result.getClass().getComponentType().equals(int.class)) {
                int[] array = (int[]) result;
                return Arrays.toString(array);
            } else if (result.getClass().getComponentType().equals(double.class)) {
                double[] array = (double[]) result;
                return Arrays.toString(array);
            } else if (result.getClass().getComponentType().equals(boolean.class)) {
                boolean[] array = (boolean[]) result;
                return Arrays.toString(array);
            } else if (result.getClass().getComponentType().equals(String.class)) {
                String[] array = (String[]) result;
                return Arrays.toString(array);
            } else {
                Object[] array = (Object[]) result;
                return Arrays.toString(array);
            }
        }

        return "" + result;
    }

    /*
    private String getString(String type, Method m, Object o, Object[] args) {
        if (type.equals("int[]")) {
            int[] results = {};//(int[])m.invoke(o, args);
            return Arrays.toString(results);
        }

        return ""+m.invoke(o, args);
    }
*/
    private String getInstanceMethodOutput(Method m, Object[] args)// throws IOException
    {
        try {
            if (c == null)
                c = m.getDeclaringClass();

            Object o = getTestInstance();

            if (o == null) {
                return "Object was not created (5)"; // errro
            }

            setupStreams();

            if (args != null)
                if (checkParameters(m, args) || m.getName().equals("main"))
                    m.invoke(o, args);
                else
                    errorMessage = "Arguments incorrect (5)";
            else
                m.invoke(o, (Object[]) null);

            String output = outContent.toString();
            cleanUpStreams();
            return output.trim();
        }
        catch(Exception e) {
            if (errorMessage.equals(""))
                errorMessage = stackToString(e);
                //errorMessage = "Method could not be invoked (5)";
        }

        if (errorMessage.equals(""))
            errorMessage = "Method does not exist (5)";

        cleanUpStreams();
        return errorMessage;
    }

     
    /**
     * This method prints the list of getter and setter methods in the class.
     * Awesome Tutorial for Getters and Setters - http://tutorials.jenkov.com/java-reflection/getters-setters.html
     * 
     * @param String name of the class where the methods are written
     * @return Nothing
     */
    public void printGettersSetters(Class aClass){
        Method[] methods = aClass.getMethods();

        for(Method method : methods){
            if(isGetter(method)) System.out.println("getter: " + method);
            if(isSetter(method)) System.out.println("setter: " + method);
        }
    }

    private boolean isGetter(Method method){
        if(!method.getName().startsWith("get"))      return false;
        if(method.getParameterTypes().length != 0)   return false;  
        if(void.class.equals(method.getReturnType())) return false;
        return true;
    }

    private boolean isSetter(Method method){
        if(!method.getName().startsWith("set")) return false;
        if(method.getParameterTypes().length != 1) return false;
        return true;
    }

    /**
     * This method checks that the desired instance variables exist, based on name and type.
     * Awesome Tutorial - http://tutorials.jenkov.com/java-reflection/private-fields-and-methods.html
     * 
     * @param String array of <<type name>> pairs, such as {"int num", "double avg"}
     * @return "pass" if they match, and an error message with information if they do not
     */
    public String testInstanceVariables(String[] fieldNames)
    {
        errorMessage = "";

        try {
            Field privateStringField;
            String[] info;
            String type, name;

            for (String field : fieldNames) {
                info = field.split(" ");
                type = info[0];
                name = info[1];

                privateStringField = c.getDeclaredField(name);

                if (privateStringField == null)
                {
                    errorMessage += "No field " + field + "\n";
                    continue;
                }

                String fieldInfo = privateStringField.toString();

                //System.out.println("privateStringField = " + privateStringField.toString());

                if (!fieldInfo.contains(name))
                    errorMessage += "Not named " + name + "\n";
                else if (!fieldInfo.contains(name))
                    errorMessage += "Not type " + type + "\n";
            }

            if (errorMessage.equals(""))
                return "pass";
        } catch (Exception e) {
            errorMessage = "fail";
        }   
        return errorMessage.trim();
    }
    
    /**
     * This method counts how many private and public instance variables are included in the class.
     * Awesome Tutorial - http://tutorials.jenkov.com/java-reflection/private-fields-and-methods.html
     * 
     * @param String name of the class
     * @return String the number of private and/or public instance variables
     */
    public String testPrivateInstanceVariables()
    {
        errorMessage = "";

        try {
            int numPrivate = 0, numPublic = 0;

            Field[] privateStringFields = c.getDeclaredFields();
            String fieldInfo = "";

            for (Field field : privateStringFields) {
                fieldInfo = field.toString();

                if (fieldInfo.contains("private"))
                    numPrivate++;
                else
                    numPublic++;
            }

            if (numPublic == 0)
                return "" + numPrivate + " Private";
            else
                return "" + numPrivate + " Private, " + numPublic + " Public";
        } catch (Exception e) {
            errorMessage = "fail";
        }   
        return errorMessage.trim();
    }

    /**
     * This method checks that instance variables of the desired type exist, without worrying about names.
     * Awesome Tutorial - http://tutorials.jenkov.com/java-reflection/private-fields-and-methods.html
     * 
     * @param String array of <<type>> values, such as {"int", "double"} in the desired order
     * @return "pass" if they match, and an error message with information if they do not
     */
    public String testInstanceVariableTypes(String[] types)
    {
        errorMessage = "";

        try {
            int count = 0;

            Field[] fields = c.getDeclaredFields();

            String found = "";

            for (Field field : fields) {
                String fieldType = field.getGenericType().toString().replace("class java.", "");
                //System.out.println("Field Type: " + fieldType);
                int j = fieldType.indexOf(".");
                if (j >=0)
                    found += fieldType.substring(j+1) + " ";
                else                
                    found += fieldType + " ";

                for (int i = 0; i < types.length; i++) {
                    if (types[i] != null && field.toGenericString().contains(types[i])) {

                        count++;
                        types[i] = null;
                        break;
                    }
                }

            }

            return found;
        } catch (Exception e) {
            errorMessage = "fail";
        }   
        return errorMessage.trim();
    }

/* Constructor Testing Code-------------------------------------------------------*/
    /**
     * This method checks that the desired instance variables exist, based on name and type.
     * Awesome Tutorial - http://tutorials.jenkov.com/java-reflection/private-fields-and-methods.html
     * 
     * @param String array of <<type name>> pairs, such as {"int num", "double avg"}
     * @return "pass" if they match, and an error message with information if they do not
     */
    public String checkDefaultConstructor() {
        return checkConstructor(0);
    }
    
    

    // adapted from https://docs.oracle.com/javase/tutorial/reflect/member/ctorInstance.html
    public String checkConstructor(Object[] args) {
        errorMessage = "";

        try {
            Constructor[] ctors = c.getDeclaredConstructors();
            Constructor ctor = null;
            for (int i = 0; i < ctors.length; i++) {
                ctor = ctors[i];
                if (args == null && ctor.getGenericParameterTypes().length == 0)
                    break;
                if (args != null && ctor.getGenericParameterTypes().length == args.length)
                    break;
            }

            try {
                ctor.setAccessible(true);
                Object obj = null;

                if (args == null)
                    obj = ctor.newInstance();
                else 
                    obj = ctor.newInstance(args);
                    
                return "pass";
            } catch (InstantiationException x) {
                errorMessage = "Could not instantiate class";
            }
        } catch (Exception e) {
            errorMessage = "fail"; //"Default Constructor does not exist";
        }

        return errorMessage;
    }
    
    public String checkConstructor(int numArgs) {
        errorMessage = "";

        try {
            Constructor[] ctors = c.getDeclaredConstructors();
            Constructor ctor = null;
            for (int i = 0; i < ctors.length; i++) {
                ctor = ctors[i];
                if (ctor.getGenericParameterTypes().length == numArgs)
                    return "pass";
            }
            
            return "fail";

        } catch (Exception e) {
            errorMessage = "fail"; //"Default Constructor does not exist";
        }

        return errorMessage;
    }

    public String checkConstructor(String argList) {
        errorMessage = "";

        int numArgs = countOccurences(argList, ",") + 1;
        argList = argList.replaceAll(" ","");

        try {
            Constructor[] ctors = c.getDeclaredConstructors();

            Constructor ctor = null;
            for (int i = 0; i < ctors.length; i++) {
                ctor = ctors[i];
                String header = ctor.toString();
                //System.out.println(ctor.toGenericString());

                if (ctor.getGenericParameterTypes().length == numArgs && header.contains(argList)) {
                    
                    return "pass";
                }
                    return "pass";
            }
            
            return "fail";

        } catch (Exception e) {
            errorMessage = "fail"; //"Default Constructor does not exist";
        }

        return errorMessage;
    }

    // https://stackoverflow.com/questions/14524751/cast-object-to-generic-type-for-returning
    private <T> T convertInstanceOfObject(Object o, Class<T> clazz) {
        try {
            return clazz.cast(o);
        } catch(ClassCastException e) {
            errorMessage = "Object could not be cast as type " + clazz.getSimpleName();
            return null;
        }
    }

    public void setDefaultValues(Object[] o) {
        defaultTestValues = o;
    }

    private Object getTestInstance() 
    {
        try {
            Constructor[] ctors = c.getDeclaredConstructors();
            Constructor ctor = null;
            Constructor shortest = ctors[0];

            for (int i = 0; i < ctors.length; i++) {
                ctor = ctors[i];
                //System.out.println(""+ ctor.getGenericParameterTypes().length);
                if (ctor.getGenericParameterTypes().length == 0) {
                    //System.out.println("Using default constructor");
                    return ctor.newInstance();
                }
                if (checkConstructorDefaults(ctor)) {
                    return ctor.newInstance(defaultTestValues);
                }
                if (ctor.getGenericParameterTypes().length < shortest.getGenericParameterTypes().length)
                    shortest = ctor;
            }

            Object[] constValues = getConstructorParameters(shortest);
            return shortest.newInstance(constValues);
        } catch (Exception e) {
            errorMessage = "Couldn't call constructor";
        }

        return null;
    }

    private boolean checkConstructorDefaults(Constructor ctor) {
        Type[] argTypes = ctor.getGenericParameterTypes();

        if (argTypes.length != defaultTestValues.length) return false;
        Type[] defTypes = getTypes(defaultTestValues);
        for (int i = 0; i < argTypes.length; i++) {
            //System.out.println(argTypes[i] + "\t" + defTypes[i]);

            if (defTypes[i] != argTypes[i])
                return false;
        }

        return true;
    }

    private Type[] getTypes(Object[] args) {
        Type[] argTypes = new Type[args.length];

        for (int i = 0; i < args.length; i++) {
            //System.out.println(args[i]);

            if (args[i] instanceof Integer) {
                argTypes[i] = Integer.TYPE;
            } else if (args[i] instanceof Double) {
                argTypes[i] = Double.TYPE;
            } else if (args[i] instanceof Boolean) {
                argTypes[i] = Boolean.TYPE;
            } else if (args[i] instanceof String) {
                argTypes[i] = String.class;
            } else if (args[i].getClass().isArray() ){
                if (args[i].getClass().getComponentType().equals(int.class)) {
                    argTypes[i] = int[].class;
                } else if (args[i].getClass().getComponentType().equals(double.class)) {
                    argTypes[i] = double[].class;
                } else if (args[i].getClass().getComponentType().equals(boolean.class)) {
                    argTypes[i] = boolean[].class;
                } else if (args[i].getClass().getComponentType().equals(String.class)) {
                    argTypes[i] = String[].class;
                } else {
                    argTypes[i] = Object[].class;
                }
            } else {
                argTypes[i] = Object.class;
            }
        }

        return argTypes;
    }

    private Object[] getConstructorParameters(Constructor ctor) {
        errorMessage = "";

        Type[] argTypes = ctor.getGenericParameterTypes();
        Object[] args = new Object[argTypes.length];

        for (int i = 0; i < argTypes.length; i++) {
            //System.out.println(args[i]);

            if (argTypes[i] == Integer.TYPE) {
                args[i] = getDefaultIntValue();
            } else if (argTypes[i] == Double.TYPE) {
                args[i] = getDefaultDoubleValue();
            } else if (argTypes[i] == Boolean.TYPE) {
                args[i] = getDefaultBooleanValue();
            } else if (argTypes[i] == String.class) {
                args[i] = getDefaultStringValue();
            /*
            } else if (args[i].getClass().isArray() ){
                if (args[i].getClass().getComponentType().equals(int.class)) {
                    argTypes[i] = int[].class;
                } else if (args[i].getClass().getComponentType().equals(double.class)) {
                    argTypes[i] = double[].class;
                } else if (args[i].getClass().getComponentType().equals(boolean.class)) {
                    argTypes[i] = boolean[].class;
                } else if (args[i].getClass().getComponentType().equals(String.class)) {
                    argTypes[i] = String[].class;
                } else {
                    argTypes[i] = Object[].class;
                }
                */
            } else {
                args[i] = new Object();
            }
        }

        return args;
    }

    private Integer getDefaultIntValue() {
        if (defaultTestValues != null) 
        {
            for (int i = 0; i < defaultTestValues.length; i++)
            {
                if (defaultTestValues[i] instanceof Integer)
                    return (Integer) defaultTestValues[i];
            }
        }
        return 10;
    }

    private Double getDefaultDoubleValue() {
        if (defaultTestValues != null) 
        {

            for (int i = 0; i < defaultTestValues.length; i++)
            {
                if (defaultTestValues[i] instanceof Double)
                    return (Double) defaultTestValues[i];
            }
        }
        return 10.0;
    }

    private Boolean getDefaultBooleanValue() {
        if (defaultTestValues != null) 
        {
            for (int i = 0; i < defaultTestValues.length; i++)
            {
                if (defaultTestValues[i] instanceof Boolean)
                    return (Boolean) defaultTestValues[i];
            }
        }
        return false;
    }

    private String getDefaultStringValue() {
        if (defaultTestValues != null) 
        {

            for (int i = 0; i < defaultTestValues.length; i++)
            {
                if (defaultTestValues[i] instanceof String)
                    return (String) defaultTestValues[i];
            }
        }
        return "Test String";
    }

/* Static Method Tests -----------------------------------------------------------*/

    private boolean displayOutput = true;
    private boolean displayErrorChecking = true;

    private String getStaticMethodOutput(Method m, Object[] arguments)// throws IOException
    {

        try {
            setupStreams();

            if (arguments != null)
                if (checkParameters(m, arguments) || m.getName().equals("main"))
                    m.invoke(null, arguments);
                else
                    errorMessage = "Arguments incorrect (3)";
            else
                m.invoke(null);

            String output = outContent.toString();
            cleanUpStreams();
            return output.trim();
        }
        catch(Exception e) {
            if (errorMessage.equals("")) {
                errorMessage = stackToString(e);
                //errorMessage += "\nMethod " + m.getName() + " could not be invoked (3)";
                
            }
        }

        if (errorMessage.equals("")) {
            //errorMessage = stackToString(e);
            errorMessage = "Method " + m.getName() + " with parameters " + Arrays.toString(arguments) + " does not exist";
        }

        cleanUpStreams();
        return errorMessage;
    }

    // https://stackoverflow.com/questions/10120709/difference-between-printstacktrace-and-tostring#:~:text=toString%20()%20gives%20name%20of,is%20raised%20in%20the%20application.&text=While%20e.,Jon%20wrote%20in%20his%20answer.
    private String stackToString(Throwable e) {
        if (e == null)  return "Exception: stack null";
    
        StringWriter sw = new StringWriter();
        e.printStackTrace(new PrintWriter(sw));

        String trace = sw.toString();

        String returnString = "";
        
        String location = "", except = "";

        String causedBy = "Caused by: ";
        int expLen = causedBy.length();
        int expStart = trace.indexOf(causedBy);

        returnString += "Start: " + expStart + "\n";

        if (expStart > -1) {
            except = trace.substring(expStart + expLen);
            //trace = trace.substring(0, expStart-1);

            int expEnd = except.indexOf(className + ".java");
            expEnd = except.indexOf("\n", expEnd);

            if (expEnd > -1)
                except = except.substring(0, expEnd);
        } else {
            return "Exception in method";
        }

        return except;
        
    }

    /** Seeing what this does
     */
    public static String getStackTraceString(Throwable e) {
        return getStackTraceString(e, "");
    }

    private static String getStackTraceString(Throwable e, String indent) {
        StringBuilder sb = new StringBuilder();
        sb.append(e.toString());
        sb.append("\n");

        StackTraceElement[] stack = e.getStackTrace();
        if (stack != null) {
            for (StackTraceElement stackTraceElement : stack) {
                sb.append(indent);
                sb.append("\tat ");
                sb.append(stackTraceElement.toString());
                sb.append("\n");
            }
        }

        Throwable[] suppressedExceptions = e.getSuppressed();
        // Print suppressed exceptions indented one level deeper.
        if (suppressedExceptions != null) {
            for (Throwable throwable : suppressedExceptions) {
                sb.append(indent);
                sb.append("\tSuppressed: ");
                sb.append(getStackTraceString(throwable, indent + "\t"));
            }
        }

        Throwable cause = e.getCause();
        if (cause != null) {
            sb.append(indent);
            sb.append("Caused by: ");
            sb.append(getStackTraceString(cause, indent));
        }

        return sb.toString();
    }

    private String getStaticMethodReturn(Method m, Object[] args)// throws IOException
    {
        try {
            if (args != null) {
                if (checkParameters(m, args)) {
                    Object result = m.invoke(null, args);
                    return cleanResult(result);
                }
                else
                    return "Arguments incorrect (2)";
            } else {
                Object result = m.invoke(null);
                return cleanResult(result);
            }
        }
        catch(Exception e) {
            if (errorMessage.equals(""))
                errorMessage = stackToString(e);
                //errorMessage = "Method " + m.getName() + " could not be invoked";
        }

        if (errorMessage.equals(""))
            errorMessage = "Method " + m.getName() + " with parameters " + Arrays.toString(args) + " does not exist";

        return errorMessage;
    }

/* Methods for getting / checking method details ---------------------------------*/
    private boolean checkStaticMethod(Method m) {

        String header = m.toGenericString();
        String[] info = header.split(" ");

        if (!info[1].equals("static")) {
            //errorMessage = "Method " + m.getName() + " is not static";
            return false;
        }

        return true;
    }

    private boolean checkReturnType(Method m, String rType) 
    {
        String header = m.toGenericString();
        String[] info = header.split(" ");

        if (checkStaticMethod(m))
            return info[2].equals(rType);

        return info[1].equals(rType);
    }

    private boolean checkParameters(Method m, Object[] arguments) 
    {
        String header = m.toGenericString().replace(className + ".", "");

        if (header.equals("public static void main(java.lang.String[])"))
            return true;

        Class<?>[] params = m.getParameterTypes();

        if (arguments == null || params == null) {
            return true;
        } 
        
        
        Class<?>[] argTypes = getArgumentTypes(arguments);        

        //System.out.println("\n***************************\nHeader: " + header + "\nClass: " + className + "\n");
        //System.out.println(m.getName());
        //System.out.println("Params: " + Arrays.toString(params) + "\nArgTypes: " + Arrays.toString(argTypes));

        if (params.length == arguments.length) {
            for (int i = 0; i < params.length; i++) {
                //System.out.println(params[i] + "\t" + argTypes[i]);
                if (params[i] != argTypes[i]) {

                    errorMessage = "Parameter and Argument types do not match";
                    return false;
                }
            }
        } else {
            errorMessage = "Parameter and Argument lengths do not match";
            return false;
        }   

        return true;
    }

    private Class<?>[] getArgumentTypes(Object[] args) {
        if (args == null)
            return null;

        Class<?>[] argTypes = new Class<?>[args.length];

        for (int i = 0; i < args.length; i++) {
            //System.out.println("Argument: " + args[i] + "\tType: ");

            if (args[i] instanceof Integer) {
                argTypes[i] = Integer.TYPE;
            } else if (args[i] instanceof Double) {
                argTypes[i] = Double.TYPE;
            } else if (args[i] instanceof Boolean) {
                argTypes[i] = Boolean.TYPE;
            } else if (args[i] instanceof String) {
                argTypes[i] = String.class;
            } else if (args[i].getClass().isArray() ){
                if (args[i].getClass().getComponentType().equals(int.class)) {
                    argTypes[i] = int[].class;
                } else if (args[i].getClass().getComponentType().equals(double.class)) {
                    argTypes[i] = double[].class;
                } else if (args[i].getClass().getComponentType().equals(boolean.class)) {
                    argTypes[i] = boolean[].class;
                } else if (args[i].getClass().getComponentType().equals(String.class)) {
                    argTypes[i] = String[].class;
                } else if (args[i].getClass().getComponentType().isArray()) {
                    if (args[i].getClass().getComponentType().equals(int[].class)) {
                        argTypes[i] = int[][].class;
                    } else if (args[i].getClass().getComponentType().equals(double[].class)) {
                        argTypes[i] = double[][].class;
                    } else if (args[i].getClass().getComponentType().equals(boolean[].class)) {
                        argTypes[i] = boolean[][].class;
                    } else if (args[i].getClass().getComponentType().equals(String[].class)) {
                        argTypes[i] = String[][].class;
                    } else {
                        argTypes[i] = Object[][].class;
                    }
                } else {
                    argTypes[i] = Object[].class;
                }
            } else {
                argTypes[i] = Object.class;
            }
        }

        return argTypes;
    }

    /* This code has been a work in progress since 2015-ish. I was stuck for
     * a long time on the testing code when a method doesn't exist.
     * Thanks to Matthew Fahrenbacher who posted his "HiddenMain" code on 
     * Facebook, I was finally able to finish it all. I am grateful that he
     * was able to help all the dominoes fall into place.
     * His files can be found here: https://repl.it/@matfah/HiddenMain 
     * and here: https://repl.it/@matfah/HiddenMain-Transparent
     */
    private String findMainMethod()
    {
        String currentDir = System.getProperty("user.dir");
        File dir = new File(currentDir);

        String[] children = dir.list();
        if(children == null)
            return "main not found";
        else
        {
            for(int i=0; i<children.length; i++)
            {
                if(children[i].endsWith(".java"))
                {
                    try
                    {
                        String clssName = children[i].substring(0,children[i].length() - ".java".length());
                        Class<?> c = Class.forName(clssName);
                        if(c != null && !clssName.equals("TestRunner") && !(replit && clssName.equals("Main"))) {
                            /*if (replit && clssName.equals("Main"))
                                continue;
                              */  
                            Method[] meths = c.getDeclaredMethods();
                            for(Method m: meths) {
                              int mods = m.getModifiers();
                              Class<?>[] params = m.getParameterTypes();

                              //we have a winner!
                              if(m.getName().equals("main") &&
                              (mods | Modifier.STATIC) == mods &&
                               m.getReturnType().getName().equals("void") &&
                               params.length == 1 &&
                               params[0] == String[].class) {
                                return m.getDeclaringClass().getName();
                              }
                            }
                        }
                    }
                    catch(Exception e)
                    {
                        e.printStackTrace();
                    }
                }
            }
        }
        return "main not found";
    }

/* Methods for checking whether code contains or does not contain a String -------*/

    public boolean checkCodeContains(String target) {
        return checkCodeContains(false, target, target, true);
    }

    public boolean checkCodeContains(String desc, String target){
        return checkCodeContains(false, desc, target, true);
    }

    public boolean checkCodeContains(String desc, String target, boolean expected)  {
        return checkCodeContains(false, desc, target, expected);
    }


    public boolean checkCodeContains(boolean useRegex, String desc, String target, boolean expected)  
    {
        String msg = "";
        String output = "";
        
        String text = getCodeWithoutComments();//getCode();
        target = removeComments(target);

        boolean hasCode = false;

        try{
            String code = text.replaceAll(" ", "");
            String target2 = target.replaceAll(" ", "");

            hasCode = code.contains(target2);

            if(!hasCode && (useRegex || isRegex(target2)))
            {
                String anyText = "[\\s\\S]*";
                target2 = createSimpleRegex(target2);

                //System.out.println(target2);
                //System.out.println(code);

                hasCode = code.matches(anyText + target2 + anyText);
            }
            
            boolean passed = expected == hasCode;

            msg = "Checking that code contains " + desc;
            output = formatOutput(""+expected, ""+hasCode, msg, passed);
            results += output + "\n";

            return passed;
        } catch (Exception e) {
            msg = "Test could not be completed";
            output = formatOutput("true", "false", msg, false);
            results += output + "\n";

        }
        return false;
    }

    public String getCode() {
        return getCodeWithoutComments();
    }

    public String getCodeWithComments() 
    {
        if (!className.contains(".java"))
            className += ".java";

        try {
            String text = new String(Files.readAllBytes(Paths.get(className)));
            return cleanQuotes(text);
        } catch (IOException e) {
            return "File " + className + " does not exist";
        }
    }

    public String getCodeWithoutComments() {
        String code = getCodeWithComments();
        code = removeComments(code);

        return code;
    }

    public String removeComments(String code) {
        int startBlock = code.indexOf("/*");
        int endBlock = -1;
        while(startBlock >= 0) {
            endBlock = code.indexOf("*/");
            if (endBlock >= 0)
                code = code.substring(0, startBlock) + code.substring(endBlock + 2);

            startBlock = code.indexOf("/*");
        }

        int startLine = code.indexOf("//");
        int endLine = -1;
        while(startLine >= 0) {
            endLine = code.indexOf("\n", startLine+1);
            if (endLine >= 0)
                code = code.substring(0, startLine) + code.substring(endLine);

            startLine = code.indexOf("//");
        }

        return code;
    }

    public boolean checkCodeContainsNoRegex(String desc, String target)  
    {
        return checkCodeContains(false, desc, target, true);
    }

    public boolean checkCodeContainsRegex(String desc, String target)  
    {
        return checkCodeContains(true, desc, target, true);
    }

    public boolean checkCodeNotContainsRegex(String desc, String target)  
    {
        return checkCodeContains(true, desc, target, false);
    }

    private boolean isRegex(String target) {
        return target.contains("*") || target.contains("$") || target.contains("#") || target.contains("~");
    }

    /**
     * Based on code from https://coderanch.com/t/401528/java/Convert-String-Regular-Expression
     */
    private String createSimpleRegex(String s) {
        StringBuilder b = new StringBuilder();
        
        for(int i=0; i<s.length(); ++i) {
            char ch = s.charAt(i);
         
            if (ch == '\n' || ch == '\r')
                b.append("\\s+");
            else if (ch == ' ')
                b.append("\\s+");
            else if (ch == '$')
                b.append("[A-Za-z]+");
            else if (ch == '#')
                b.append("[0-9A-Za-z*-+/ \\(\\)]+");
                else if (ch == '?')
                b.append("[<>=!?]+");
            else if (ch == '~')
                b.append("[+-=]+[0-9]*");
            else if (ch == '*')
                b.append("[A-Za-z0-9 <>=!+/\\-*\\(\\)]+");
            else if ("\\.^$|?*+[]{}()".indexOf(ch) != -1)
                b.append('\\').append(ch);
            else
                b.append(ch);
        }        
        
        return b.toString();
    }
    
    public boolean checkCodeNotContains(String target) {
        return checkCodeNotContains(target, target);
    }

    public boolean checkCodeNotContains(String desc, String target) 
    {
        return checkCodeContains(false, desc, target, false);
    }

    public boolean codeChanged(String origCode)
    {
        return codeChanged(origCode, true);
    }

    public boolean codeChanged(String origCode, boolean expected) 
    {
        String msg = "";
        String output = "";
        
        String currCode = getCode();
        origCode = removeComments(origCode);

        try{
            currCode = currCode.replaceAll("\\s+", "");
            origCode = origCode.replaceAll("\\s+", "");
            //System.out.println(origCode);
            //System.out.println("*****************");
            //System.out.println(text);

            boolean changed = !currCode.equals(origCode);
            boolean passed = changed == expected;
            msg = "Checking that code has been changed";

            output = formatOutput(""+expected, ""+changed, msg, passed);
            results += output + "\n";
        
            return passed;
        } catch (Exception e) {
            msg = "Test could not be completed";
            output = formatOutput("true", "false", msg, false);
            results += output + "\n";

        }
        
        return false;
    }

/* Methods for dealing with output streams ---------------------------------------*/

    /**
     * Sets up the test fixture. Saves the standard output streams.
     *
     * Called before every test case method.
     */
    @Before
    public void setUp() throws IOException
    {
        stdOut = System.out;
        stdErr = System.err;
    }

    /**
     * Tears down the test fixture. Restores the standard output streams.
     *
     * Called after every test case method.
     */
    @After
    public void tearDown()
    {
        cleanUpStreams();
    }

    public void setupStreams()
    {
        stdOut = System.out;
        stdErr = System.err;
        System.setOut(new PrintStream(outContent));
        outContent.reset();

    }

    public void cleanUpStreams()
    {
        System.setOut(stdOut);
        System.setErr(stdErr);
    }

    static final ByteArrayOutputStream outContent = new ByteArrayOutputStream();
    static final ByteArrayOutputStream errContent = new ByteArrayOutputStream();
    static PrintStream stdOut;
    static PrintStream stdErr;

/* Formatting Methods ------------------------------------------------------------*/

    

    protected String cleanString(String orig)   //\\s+
    {
        return orig.replaceAll("\\s+"," ").replaceAll("[^A-Za-z0-9 ]", "").trim();
    }

    protected String cleanStringIgnoreCase(String orig)   //\\s+
    {
        return cleanString(orig.toLowerCase());
    }



/* Random helper methods so they don't have to be rewritten lots of times
*/
    public String removeSpaces(String orig) {
        return orig.replaceAll("\\s+", "");
    }

    public String removeNewLines(String orig) {
        return orig.replaceAll("\n", "").replaceAll("\r", "");
    }

    public static int countOccurences(String orig, String target) {
        orig = orig.replaceAll("\\s+", "");
        target = target.replaceAll("\\s+","");

        int count = 0;

        int index = orig.indexOf(target);

        while (index > -1) {
            count ++;
            index = orig.indexOf(target, index + 1);
        }
        return count;
    } 

    public int countOccurencesRegex(String orig, String target) {

        

        orig = orig.replaceAll("\\s+", "");
        target = target.replaceAll("\\s+","");

        target = createSimpleRegex(target);

        int count = 0;
        int pos = 0;

        Pattern p = Pattern.compile(target);
        Matcher m = p.matcher(orig);
        
        //System.out.println(p);
        //System.out.println(m);
        //System.out.println(pos + "\t" + m.find(pos));
        

        while (m.find(pos)) {
            pos = m.start() + 1;
            //System.out.println(pos + "\t" + m.find(pos));
            count++;
        }
        return count;
    }

    public boolean containsIgnoreCase(String orig, String target){
        return orig.toLowerCase().contains(target.toLowerCase());
    }

    public boolean isMatch(String orig, String target) {
        target = target.replaceAll("\\s", "");
        orig = orig.replaceAll("\\s", "");
        
        if(isRegex(target))
        {
            target = createSimpleRegex(target);

            //System.out.println(target);

            return orig.matches(target);
        }

        return orig.contains(target);

    }

    public boolean containsMatch(String orig, String target) {
        target = target.replaceAll("\\s", "");
        orig = orig.replaceAll("\\s", "");
        
        if(isRegex(target))
        {
            String anyText = "[\\s\\S]*";
            target = createSimpleRegex(target);

            //System.out.println(target);

            return orig.matches(anyText + target + anyText);
        }

        return orig.contains(target);

    }

/* With input methods .......................... */

    private ByteArrayInputStream inContent;

    public String getMethodOutputWithInput(String methodName, String input) {
        inContent = new ByteArrayInputStream(input.getBytes(StandardCharsets.UTF_8));
        System.setIn(inContent);
        
        String output = getMethodOutput(methodName);

        System.setIn(System.in);

        return output;
    }


    

    public String cleanQuotes(String str) {
        return str.replaceAll("[\\u2018\\u2019]", "'")
           .replaceAll("[\\u201C\\u201D]", "\"");
    }

    public static void sortResults() {
        String newResults = "";
        int size = countOccurences(results, "Expected:");
        String[] tests = new String[size];
        int[] values = new int[size];
        int start = 0, end = 0;

        for (int i = 0; i < size; i++) {
            values [i] = i;
            end = results.indexOf("Expected:", start + 1);
            if (end >= 0)
                tests[i] = results.substring(start, end);
            else
                tests[i] = results.substring(start);
            start = end;
        }

        

        for (int i = 0; i < size; i++) {
            String currMsg = tests[i].substring(tests[i].indexOf("Message: ")).toLowerCase();
            int min = i;

            for (int j = i + 1; j < size; j++) {
                String nextMsg = tests[j].substring(tests[j].indexOf("Message: ")).toLowerCase();
                if (nextMsg.compareTo(currMsg) < 0)
                    min = j;
            }

            int temp = values[i];
            values[i] = values[min];
            values[min] = temp;

            
        }

        for (int i = 0; i < size; i++) {
            newResults += tests[values[i]];
        }

        results = newResults;
    }
}