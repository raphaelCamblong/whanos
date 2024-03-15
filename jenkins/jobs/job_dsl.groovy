import java.io.File

/* get all available languages */
def directory_images = new File('/var/jenkins_home/resource/images')
File[] sub_directory = directory_images.listFiles().findAll { it.isDirectory() };
def available_languages = sub_directory.collect { it.name }

println "Available languages: " + available_languages


/* BUILD IMAGES JOBS*/
folder('/Whanos base images') {
    description('Base images for Whanos')
}

for (language in available_languages) {
    job("/Whanos base images/whanos-${language}") {
        wrappers {
            colorizeOutput()
            timestamps()
        }
        steps {
            shell("echo 'Start Building ${language} Base images'")
            shell("python3 \$JENKINS_RESOURCE/scripts/smart_build.py build-base-image ${language} \$JENKINS_RESOURCE/images")
        }
    }
}

freeStyleJob('/Whanos base images/Build all base images') {
    publishers {
        downstream(available_languages.collect { language -> "Whanos base images/whanos-$language" })
	}
}

/*LINK PROJECT JOBS*/

folder("Projects") {
}

freeStyleJob("link-project") {
    displayName('Link project')
    description('Link project to Jenkins')
    parameters {
        stringParam('REPOSITORY_URL', '', 'Link to project: \n user/repository (do not put https/... or .git)')
        stringParam('PROJECT_NAME', '', 'Name of project')
    }
    steps {
        dsl {
            text("""
                freeStyleJob("Projects/\$PROJECT_NAME") {
                    displayName("\$PROJECT_NAME")
                    description("Project \$PROJECT_NAME")
                    scm {
                        git {
                            remote {
                                github("\$REPOSITORY_URL")
                                credentials('github-organization-credentials')
                            }
                        }
                    }
                    triggers {
                        scm('*/1 * * * *')
                    }
                    environmentVariables {
                        env("REPOSITORY_URL", "\$REPOSITORY_URL")
                        env("PROJECT_NAME", "\$PROJECT_NAME")
                    }
                    steps {
                        shell('ls -la')
                        shell('python3 \$JENKINS_RESOURCE/scripts/whanos_tool.py . \$BUILD_NUMBER \$JENKINS_RESOURCE/scripts/language_detection_rules.json \$JENKINS_RESOURCE/images \$JENKINS_RESOURCE/helm')
                        shell('cat values.yaml')
                    }
                }""".stripIndent())
        }
    }
}
