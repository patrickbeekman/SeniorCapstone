/**
 * Created by patt on 2/12/18.
 */
//creating an application module
var studentAppModule = angular.module("StudentCtrl", []);

//The below code will read the data from student.json file and will pass to the $scope variable
studentAppModule.controller("StudentController", function($scope, $http){
            $http.get('students.json') //reading the student.json file

                .success (function(data){
                        console.log(data);
                        $scope.students = data; // binding the data to the $scope variable
                    })
                .error(function(data, status) {
                        console.error('failure loading the student record', status, data);
                        $scope.students = { }; //return blank record if something goes wrong
                });
    }
);//end controller